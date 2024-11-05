# ------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* /
COPY ./app /app
COPY ./fastapi_logging.json /app/fastapi_logging.json

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir poetry && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install --no-cache-dir --no-deps -r requirements.txt
# ------------------------------------------------------------
FROM python:3.12-slim AS production

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
COPY --from=builder /app/fastapi_logging.json /app/fastapi_logging.json

EXPOSE 9999
# ------------------------------------------------------------
ENV HL_LOGGING_CONFIG_PATH=/app/fastapi_logging.json
CMD ["/opt/venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9999", "--reload"]
