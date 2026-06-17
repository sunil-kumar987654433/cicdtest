import os
from celery.app import Celery
from src.config import Config


celery_app = Celery(
    __name__, 
    broker=Config.CELERY_BROKER_URL, 
    backend=Config.CELERY_BACKEND_URL,
    include=["src.account.task"]
    )


celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    result_extended=True,
)