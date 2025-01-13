from celery import Celery

# Create a Celery instance
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # Redis as the message broker
    backend='redis://localhost:6379/0'  # Redis as the result backend
)

@celery.task
def add(x, y):
    return x + y
