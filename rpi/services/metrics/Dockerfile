# ------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* /

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir poetry && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install --no-cache-dir --no-deps -r requirements.txt
# ------------------------------------------------------------
FROM python:3.12-slim AS production

RUN apt update && apt upgrade -y && apt install network-manager -y

COPY --from=builder /opt/venv /opt/venv
COPY ./alembic.ini /alembic.ini
COPY ./alembic /alembic
COPY ./app /app

EXPOSE 9999
ENV PYTHONPATH=/
# ------------------------------------------------------------
CMD ["/opt/venv/bin/python", "-m", "uvicorn", "app.webserver:app", "--host", "0.0.0.0", "--port", "9999", "--reload"]
