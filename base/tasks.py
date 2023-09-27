import os
from datetime import date, timedelta

from celery import shared_task, Celery
#from django.contrib.sites import requests
import requests
from rest_framework import serializers

from base.models import NASAApod
from base.serializers import ApodSerializer
from externalapiproject.settings import URL, NASA_API_KEY
import time
from pictures.models import Image


@shared_task
def fetch_and_save_nasa_data():
    '''
    We want to create a task which will save data of every date available
    So in turn nasa gets new data everyday for APOD
    First start from earliest date and save everything then schedule it to run and save every day at a specific time when NASA uploads data to the API
    '''

    base_url = URL
    api_key = NASA_API_KEY

    start_date = date(2002,1,8)
    #print('startdate', start_date)
    #end_date = date.today()
    end_date = date(2003,6,16)
    #print('enddate', end_date)

    date_format = '%Y-%m-%d'

    current_date = start_date
    #print('current date', current_date)
    while current_date <= end_date:
        formatted_date = current_date.strftime(date_format)
        url = f'{base_url}?api_key={api_key}&date={formatted_date}'
        #response = requests.get(url)
        #data = response.json()
        #response_date = data.get('date')

        if not NASAApod.objects.filter(date=current_date).exists():
            print('url',url)
            response = requests.get(url)
            #print('API Response', response)
            data = response.json()
            print('data',data)

            if 'code' in data and data['code'] == 400:
                continue
            print('date',current_date)
            explanation = data.get('explanation')
            hdurl = data.get('hdurl')
            media_type = data.get('media_type')
            service_version = data.get('service_version')
            title = data.get('title')
            url = data.get('url')

            apod_data = {
                'date': current_date,
                'explanation': explanation,
                'hdurl': hdurl,
                'media_type': media_type,
                'service_version': service_version,
                'title': title,
                'url': url,
            }
            #print('response which will be saved', apod_data)
            try:

                serializer = ApodSerializer(data=apod_data)
                if serializer.is_valid():
                    serializer.save()
            except serializers.ValidationError as e:
                print(e.detail)
                # response.data = e.detail

        current_date += timedelta(days=1)
        time.sleep(500)




