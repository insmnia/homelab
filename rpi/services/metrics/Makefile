run:
	poetry run uvicorn app.webserver:app --reload --host 0.0.0.0 --port 9999 --access-log
tasks:
	poetry run python ./app/scheduler.py
migration:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
ruff-check:
	ruff check . --ignore E731
