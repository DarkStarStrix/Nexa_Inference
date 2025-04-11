# app/gunicorn.conf.py
from app.config import settings

bind = "0.0.0.0:8000"
workers = settings.MAX_WORKERS
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
errorlog = "-"
accesslog = "-"
loglevel = settings.LOG_LEVEL.lower()