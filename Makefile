ALEMBIC ?= alembic
STEP ?= -1

.PHONY: db-revision db-upgrade db-downgrade db-current db-history db-drift-check

db-revision:
	@if [ -z "$(message)" ]; then echo "Usage: make db-revision message=\"your message\""; exit 1; fi
	$(ALEMBIC) revision --autogenerate -m "$(message)"

db-upgrade:
	$(ALEMBIC) upgrade head

db-downgrade:
	$(ALEMBIC) downgrade $(or $(step),$(STEP))

db-current:
	$(ALEMBIC) current

db-history:
	$(ALEMBIC) history

db-drift-check:
	$(ALEMBIC) check
