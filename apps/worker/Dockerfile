FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/apps/api:/app/apps/worker

WORKDIR /app

COPY apps/api/requirements.txt /app/apps/api/requirements.txt
COPY apps/worker/requirements.txt /app/apps/worker/requirements.txt
RUN pip install --no-cache-dir -r /app/apps/worker/requirements.txt

COPY apps/api /app/apps/api
COPY apps/worker /app/apps/worker

WORKDIR /app/apps/worker
CMD ["celery", "-A", "worker_app.celery_app", "worker", "--loglevel=info", "-Q", "tts"]

