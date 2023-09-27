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
import json


#app = Celery('tasks', broker='redis://localhost:6379/0')
# app = Celery('d_c_p2')

#@shared_task
#@app.task
#@shared_task

@shared_task
def fetch_and_save_pickup_lines():
    api_url1 = PICKUP_URL
    api_url2 = PICKUP2_URL

    pickup1 = get_pickup_text(api_url1)
    pickup2 = get_pickup_json(api_url2)
    #print('pickup1', pickup1)
    #print('pickup2', pickup2)

    pickup_data = {
        'pickup1': pickup1,
        'pickup2': pickup2,
    }


    pickup_data_json = json.dumps(pickup_data)
    #print(pickup_data_json)


    save_pickup_data_to_db(pickup_data_json)
    #print("Pickup data saved to db succesfully")


def save_pickup_data_to_db(pickup_data_json):
    pickup_data = json.loads(pickup_data_json)
    #print(pickup_data)

    pickup1 = pickup_data['pickup1']
    pickup2 = pickup_data['pickup2']

    if not PickupData.objects.filter(text=pickup1).exists():
        PickupData.objects.create(text=pickup1)

    if not PickupData.objects.filter(text=pickup2).exists():
        PickupData.objects.create(text=pickup2)

        #print("Data saved successfully")

# def fetch_and_save_pickup_lines():
#     api_url1 = PICKUP_URL
#     api_url2 = PICKUP2_URL
#
#     pickup1 = get_pickup_text(api_url1)
#     pickup2 = get_pickup_json(api_url2)
#
#     # PickupData.objects.create(text=pickup1)
#     # PickupData.objects.create(text=pickup2)
#     pickup1 = get_pickup_text(api_url1)
#     pickup2 = get_pickup_json(api_url2)
#
#     if not PickupData.objects.filter(text=pickup1).exists():
#         PickupData.objects.create(text=pickup1)
#
#     if not PickupData.objects.filter(text=pickup2).exists():
#         PickupData.objects.create(text=pickup2)

# @shared_task
# def update_pickup_lines_periodically():
#     # Schedule the task to run every hour
#     fetch_and_save_pickup_lines.apply_async(eta=timezone.now() + timedelta(minutes=1))
#
def get_pickup_text(url):
    response = requests.get(url)
    return response.text

def get_pickup_json(url):
    response = requests.get(url)
    data = response.json()
    pickup_value = data.get('pickup', '').strip()
    # Create a dictionary with a 'pickup' key and the pickup_value as the value
    return pickup_value

# #To run every hour
# app.conf.beat_schedule = {
#     'update-pickup-lines' : {
#         'task': 'pickup.tasks.update_pickup_lines_periodically',
#         'schedule': crontab(minute=0, hour='*/1'),
#     },
# }