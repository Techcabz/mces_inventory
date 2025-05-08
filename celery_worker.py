from app import create_app
from app.extensions import celery
from celery_config import init_celery

app = create_app()
init_celery(app)
