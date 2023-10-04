import json
import random

import requests
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import DeviceAnalytics
from externalapiproject.settings import PICKUP_URL
from externalapiproject.settings import PICKUP2_URL
from pickup.models import PickupData
# from .tasks import fetch_and_save_pickup_lines, update_pickup_lines_periodically
from ip2geotools.databases.noncommercial import DbIpCity
import socket


class Rizz(APIView):
    # def get(self, request, **kwargs):
    #     api_url1 = PICKUP_URL
    #     api_url2 = PICKUP2_URL
    #     pickup1 = self.get_pickup_text(PICKUP_URL)
    #     pickup2 = self.get_pickup_json(PICKUP2_URL)
    #
    #     if PickupData.objects.filter(text=pickup1).exists():
    #         pickup1_exists = True
    #     else:
    #         PickupData.objects.create(text=pickup1)
    #         pickup1_exists = False
    #
    #     if PickupData.objects.filter(text=pickup2).exists():
    #         pickup2_exists = True
    #     else:
    #         PickupData.objects.create(text=pickup2)
    #         pickup2_exists = False
    #
    #     all_the_pickup_lines = PickupData.objects.values_list('text', flat=True)
    #     random_line = random.choice(all_the_pickup_lines)
    #
    #     return Response(random_line, content_type='text/plain', status=status.HTTP_200_OK)
    #
    # def get_pickup_text(self, url):
    #     response = requests.get(url)
    #     return response
    #
    # def get_pickup_json(self, url):
    #     response = requests.get(url)
    #     data = response.json()
    #     return data.get('pickup', '').strip()

    #I am getting 4 fields null then retireve city , country and ip
    #Increase count every time request is made
    #One more thing is there could be a device type as iphone but the widget family could be
    #Widget size small for app pickup but for shayari the widget size could be large so we need to join these
    #Like for device type iphone widget size - small , large should be stored in a list
    #Create analytics app and make model with data sent from didi
    #Analytics data from all endpoints will go in this model

    #pickup_count = 0;

    def post(self, request):
        device_type = request.data.get('device_type')
        os_version = request.data.get('os_version')
        device_id = request.data.get('device_id')
        widget_family = request.data.get('widget_family')

        if device_type is not None and os_version is not None and device_id is not None and widget_family is not None:
            device_analytics = {
                'device_type' : device_type,
                'os_version' : os_version,
                'device_id' : device_id,
                'widget_family' : widget_family,
            }

            existing_device_id = DeviceAnalytics.objects.filter(device_id=device_id).first()

            with transaction.atomic():
                if existing_device_id:
                    if existing_device_id.PickupCount is not None:
                        existing_device_id.PickupCount += 1
                        existing_device_id.save()
                    else:
                        existing_device_id.PickupCount = 1
                        existing_device_id.save()
                    if existing_device_id.widget_family:
                        existing_widget_family_list = existing_device_id.widget_family.split(',')
                        if widget_family not in existing_widget_family_list:
                            existing_device_id.widget_family += f',{widget_family}'
                            existing_device_id.save()
                    else:
                        existing_device_id.widget_family = widget_family
                        existing_device_id.save()
                else:
                    device_analytics = DeviceAnalytics(**device_analytics)
                    device_analytics.save()

            all_the_pickup_lines = PickupData.objects.values_list('text', flat=True)
            random_line = random.choice(all_the_pickup_lines)
            return Response(random_line, content_type='application/json', status=status.HTTP_201_CREATED)

        else:
            ip_address = request.META.get('REMOTE_ADDR')
            Location = DbIpCity.get(ip_address, api_key='free')
            city = Location.city
            country = Location.country
            device_analytics = {
                'ip' : ip_address,
                'city' : city,
                'country' : country,
            }

            existing_device_id = DeviceAnalytics.objects.filter(device_id=device_id).first()

            with transaction.atomic():
                if existing_device_id:
                    if existing_device_id.PickupCount is not None:
                        existing_device_id.PickupCount += 1
                        existing_device_id.save()
                    else:
                        existing_device_id.PickupCount = 1
                        existing_device_id.save()
                        if existing_device_id.widget_family:
                            existing_widget_family_list = existing_device_id.widget_family.split(',')
                            if widget_family not in existing_widget_family_list:
                                existing_device_id.widget_family += f',{widget_family}'
                                existing_device_id.PickupCount += 1
                                existing_device_id.save()
                        else:
                            existing_device_id.widget_family = widget_family
                            existing_device_id.PickupCount += 1
                            existing_device_id.save()
                else:
                    device_analytics = DeviceAnalytics(**device_analytics)
                    device_analytics.save()

            all_the_pickup_lines = PickupData.objects.values_list('text', flat=True)
            random_line = random.choice(all_the_pickup_lines)
            return Response(random_line, content_type='application/json', status=status.HTTP_201_CREATED)