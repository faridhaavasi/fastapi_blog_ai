# python
import os
from dotenv import load_dotenv

# celery
from celery import Celery

# loading .env file content
load_dotenv()

# getting redis url broker and backend url
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# setting up celery_app instance
celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# use the code below to add task to celery beat

# celery_app.conf.beat_schedule = {
#     "sample-task": {
#         "task": "service.celery_config.celery_task.sample_task",
#         "schedule": 10.0,  # every 10 seconds
#     },
# }

# setting time zone
celery_app.conf.timezone = "UTC"

# making the celery to know where he should look for tasks
celery_app.autodiscover_tasks(["service.celery_config.celery_task"])