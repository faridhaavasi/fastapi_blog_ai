# python
import os
from dotenv import load_dotenv

# celery
from celery import Celery

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.beat_schedule = {
    "sample-task": {
        "task": "service.celery_config.celery_task.sample_task",
        "schedule": 10.0,  # every 10 seconds
    },
}
celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(["service.celery_config.celery_task"])