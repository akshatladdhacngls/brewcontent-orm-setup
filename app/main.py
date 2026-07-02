from fastapi import FastAPI

app = FastAPI(title="Microservice ORM Base")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
