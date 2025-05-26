import os
from celery import Celery
from core.config import settings



broker_url = getattr(settings, "CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = getattr(settings, "CELERY_RESULT_BACKEND", broker_url)

celery_app = Celery(
    'fuzzy_search',
    broker=broker_url,
    backend=result_backend,
    include=['services.task']
)

# чтобы разрешить update_state(state='STARTED')
celery_app.conf.task_track_started = True
