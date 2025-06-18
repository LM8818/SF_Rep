# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base               # минимальный образ[10]
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser                                 # non-root[10]

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", \
     "--bind", "0.0.0.0:8000", "--workers", "4", "--proxy-headers"]
