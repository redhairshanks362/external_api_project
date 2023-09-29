import calendar
import random
import re
from datetime import date, timedelta, datetime
import time

from celery import shared_task
from django.core.serializers import json

#from django.contrib.sites import requests

from externalapiproject.settings import NUMBER_API_URL
from numbers_api import serializers
from numbers_api.models import Number
from numbers_api.serializers import NumberSerializer
import requests
from datetime import datetime

@shared_task()
def fetch_and_save_date_specific_data():
    api_url = NUMBER_API_URL
    for kwarg_month in range(1, 12):
        days_in_month = calendar.monthrange(2023, kwarg_month)[1]
        for kwarg_date in range(1, days_in_month + 1):
            url = f'{api_url}/{kwarg_month}/{kwarg_date}/date'
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    fact_text = response.text
                    #print('response', response)
                    #print('url', url)

                    #date_str =
                    match = re.search(r'(\w+)\s(\d+)(?:st|nd|rd|th)', fact_text)
                    if match:
                        month_name = match.group(1)
                        day = int(match.group(2))

                    month_dict = {
                        'January': 1,
                        'February': 2,
                        'March': 3,
                        'April': 4,
                        'May': 5,
                        'June': 6,
                        'July': 7,
                        'August': 8,
                        'September': 9,
                        'October': 10,
                        'November': 11,
                        'December': 12,
                    }

                    month = month_dict.get(month_name)

                    # Check if the fact_text already exists in the database
                    existing_record = Number.objects.filter(fact_text=fact_text).first()
                    if not existing_record:
                        response_data = {'fact_text':fact_text,'month':month,'day':day}
                        serializer = NumberSerializer(data=response_data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(f"Serializer error: {serializer.errors}")

                except Exception as e:
                    print(f"Error processing API response: {e}")
            else:
                print(f"API request failed with status code: {response.status_code}")
                print(f"Response content: {response.text}")

        time.sleep(300)

