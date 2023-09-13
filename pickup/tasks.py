from datetime import timedelta
from django.utils import timezone

from celery import shared_task, Celery
from celery.loaders import app
from celery.schedules import crontab
from .models import PickupData
import requests
import random
from externalapiproject.settings import PICKUP_URL
from externalapiproject.settings import PICKUP2_URL


#app = Celery('tasks', broker='redis://localhost:6379/0')
app = Celery('externalapiproject')

#@shared_task
@app.task
def fetch_and_save_pickup_lines():
    api_url1 = PICKUP_URL
    api_url2 = PICKUP2_URL

    pickup1 = get_pickup_text(api_url1)
    pickup2 = get_pickup_json(api_url2)

    PickupData.objects.create(text=pickup1)
    PickupData.objects.create(text=pickup2)

@shared_task
def update_pickup_lines_periodically():
    # Schedule the task to run every hour
    fetch_and_save_pickup_lines.apply_async(eta=timezone.now() + timedelta(hours=1))



def get_pickup_text(self, url):
    response = requests.get(url)
    return response

def get_pickup_json(self, url):
    response = requests.get(url)
    data = response.json()
    return data.get('pickup', '').strip()

#To run every hour
app.conf.beat_schedule = {
    'update-pickup-lines' : {
        'task': 'pickup.tasks.update_pickup_lines_periodically',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}