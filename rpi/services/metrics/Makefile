run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 9999 --access-log
migration:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
ruff-check:
	ruff check . --ignore E731
