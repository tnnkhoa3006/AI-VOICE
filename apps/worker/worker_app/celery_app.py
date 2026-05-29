from app.queue import celery_app

import worker_app.tasks  # noqa: F401

__all__ = ["celery_app"]

