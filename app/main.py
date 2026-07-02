from __future__ import annotations

import uuid

from duckduckgo_search import DDGS
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import SearchJob, SearchResult
from app.db.session import get_db

app = FastAPI(title="Web Search Agent PoC")


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    max_results: int = Field(default=5, ge=1, le=10)


class SearchResponse(BaseModel):
    id: uuid.UUID
    query: str
    status: str
    result_count: int
    error_message: str | None = None


class SearchResultItem(BaseModel):
    rank: int
    title: str
    url: str
    snippet: str | None
    source: str


class SearchJobDetail(SearchResponse):
    results: list[SearchResultItem]


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse, tags=["search"])
def run_search(payload: SearchRequest, db: Session = Depends(get_db)) -> SearchResponse:
    job = SearchJob(query=payload.query, status="running")
    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        with DDGS() as ddgs:
            records = list(ddgs.text(payload.query, max_results=payload.max_results))

        for index, record in enumerate(records, start=1):
            db.add(
                SearchResult(
                    job_id=job.id,
                    rank=index,
                    title=record.get("title") or "Untitled",
                    url=record.get("href") or "",
                    snippet=record.get("body"),
                    source="duckduckgo",
                )
            )

        job.status = "completed"
        job.result_count = len(records)
    except Exception as exc:
        job.status = "failed"
        job.error_message = str(exc)

    db.add(job)
    db.commit()
    db.refresh(job)

    return SearchResponse(
        id=job.id,
        query=job.query,
        status=job.status,
        result_count=job.result_count,
        error_message=job.error_message,
    )


@app.get("/search/{job_id}", response_model=SearchJobDetail, tags=["search"])
def get_search_job(job_id: uuid.UUID, db: Session = Depends(get_db)) -> SearchJobDetail:
    query = (
        select(SearchJob)
        .options(selectinload(SearchJob.results))
        .where(SearchJob.id == job_id)
    )
    job = db.scalar(query)
    if job is None:
        raise HTTPException(status_code=404, detail="Search job not found")

    items = [
        SearchResultItem(
            rank=item.rank,
            title=item.title,
            url=item.url,
            snippet=item.snippet,
            source=item.source,
        )
        for item in sorted(job.results, key=lambda row: row.rank)
    ]

    return SearchJobDetail(
        id=job.id,
        query=job.query,
        status=job.status,
        result_count=job.result_count,
        error_message=job.error_message,
        results=items,
    )
