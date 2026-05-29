from celery import Celery

from app.core.config import settings

celery_app = Celery(
  "mimo_voice_studio",
  broker=settings.redis_url,
  backend=settings.redis_url,
)

celery_app.conf.task_routes = {
  "worker.generate_tts_audio": {"queue": "tts"},
}

