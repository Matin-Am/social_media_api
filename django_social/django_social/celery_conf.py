import os 
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_social.settings')
app = Celery("django_social")

app.conf.broker_url = "amqp://matin:matin@localhost:5672/matin_vhost"
app.conf.task_serializer = "json"
app.conf.accept_content = ["json",]
app.conf.worker_prefetch_multiplier = 1
app.conf.task_ignore_result = True
app.conf.task_acks_late = True

app.autodiscover_tasks()