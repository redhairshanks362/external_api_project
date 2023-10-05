import os
import re
from datetime import date, timedelta

from celery import shared_task, Celery
#from django.contrib.sites import requests
import requests
from django.utils import timezone
from rest_framework import serializers

from base.models import NASAApod
from base.serializers import ApodSerializer
from externalapiproject.settings import URL, NASA_API_KEY, NASA_API_KEY2
import time
from pictures.models import Image


#This approach calls the NASA API for each date in the date range and then check if that date is available in the database which is inefficient and causes 429 response
'''
@shared_task
def fetch_and_save_nasa_data():
    
    We want to create a task which will save data of every date available
    So in turn nasa gets new data everyday for APOD
    First start from earliest date and save everything then schedule it to run and save every day at a specific time when NASA uploads data to the API
    

    base_url = URL
    api_key = NASA_API_KEY
    #api_key = NASA_API_KEY2

    start_date = date(2020,9,30)
    #print('startdate', start_date)
    #end_date = date.today()
    end_date = date(2023,9,29)
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
            print(f"The data for {current_date} doesn't exist so saving it in db")
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
        #Uncomment this after fetching data is complete
        else:
            print(f"The data for {current_date} exists or is not available with NASA so skipping the date and moving to the next date")
            current_date += timedelta(days=1)
            continue

        current_date += timedelta(days=1)
        #time.sleep(100)
        '''

#check if each date is already in the database and only make API requests for the missing dates
@shared_task
def fetch_and_save_nasa_data():
    base_url = URL
    api_key = NASA_API_KEY
    start_date = timezone.localdate()
    end_date = date(1995, 6, 16)
    date_format = '%Y-%m-%d'

    current_date = start_date

    # Get the list of dates that are already in the database
    existing_dates = NASAApod.objects.values_list('date', flat=True)

    while current_date >= end_date:
        formatted_date = current_date.strftime(date_format)

        # Check if the date is already in the database
        if current_date in existing_dates:
            print(f"The data for {current_date} already exists in the database, skipping...")
        else:
            url = f'{base_url}?api_key={api_key}&date={formatted_date}'
            print(f"Fetching data for {current_date} from NASA API")

            response = requests.get(url)
            data = response.json()

            if 'code' in data and data['code'] == 400:
                if 'msg' in data:
                    date_pattern = re.search(r"No data available for date", data['msg'])
                    if date_pattern:
                        missing_date = date_pattern.group(1)
                        print(f"External API doesn't have data for {missing_date}")
                continue

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

            try:
                serializer = ApodSerializer(data=apod_data)
                if serializer.is_valid():
                    serializer.save()
                    print(f"Data for {current_date} saved in the database")
            except serializers.ValidationError as e:
                print(e.detail)

        current_date += timedelta(days=1)
        time.sleep(500)







