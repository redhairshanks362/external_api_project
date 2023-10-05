import json
import random

import requests
from django.db import transaction
from django.db.models import F, Sum, Max
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import DeviceAnalytics, PickupAnalytics
from externalapiproject.settings import PICKUP_URL
from externalapiproject.settings import PICKUP2_URL
from pickup.models import PickupData
# from .tasks import fetch_and_save_pickup_lines, update_pickup_lines_periodically
from ip2geotools.databases.noncommercial import DbIpCity
import socket


class Rizz(APIView):
    '''
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
    '''

    #I am getting 4 fields null then retireve city , country and ip
    #Increase count every time request is made
    #One more thing is there could be a device type as iphone but the widget family could be
    #Widget size small for app pickup but for shayari the widget size could be large so we need to join these
    #Like for device type iphone widget size - small , large should be stored in a list
    #Create analytics app and make model with data sent from didi
    #Analytics data from all endpoints will go in this model

    #pickup_count = 0;
    #H

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

            all_the_pickup_id = PickupData.objects.values_list('id', flat=True)
            random_id = random.choice(all_the_pickup_id)
            random_pickup = PickupData.objects.get(id=random_id)
            random_line = random_pickup.text
            #random_line = "Are you cryptocurrency? Coz I wanna hold you for so long."

            #Updating count for the specific pickup line
            #First making a filter to check if the pickup line for the device id has a count if it does increase it by 1
            pickup_entry = PickupAnalytics.objects.filter(pickup_data__text = random_line, analytics__device_id = device_id).first()
            if pickup_entry:
                PickupAnalytics.objects.filter(pk=pickup_entry.pk).update(count=F('count') + 1)
            #Otherwise create a count for that and add it
            else:
                analytics_entry = DeviceAnalytics.objects.filter(device_id = device_id).first()
                pickup_entry = PickupData.objects.filter(text=random_line).first()
                if analytics_entry and pickup_entry:
                    PickupAnalytics.objects.create(analytics = analytics_entry, pickup_data = pickup_entry, count = 1)
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

            all_the_pickup_id = PickupData.objects.values_list('id', flat=True)
            random_id = random.choice(all_the_pickup_id)
            random_pickup = PickupData.objects.get(id=random_id)
            random_line = random_pickup.text
            #random_line = "Are you cryptocurrency? Coz I wanna hold you for so long."
            #Updating count for the specific pickup line
            #First making a filter to check if the pickup line for the device id has a count if it does increase it by 1
            pickup_entry = PickupAnalytics.objects.filter(pickup_data__text = random_line, analytics__device_id = device_id).first()
            if pickup_entry:
                PickupAnalytics.objects.filter(pk=pickup_entry.pk).update(count=F('count') + 1)
            #Otherwise create a count for that and add it
            else:
                analytics_entry = DeviceAnalytics.objects.filter(device_id = device_id).first()
                pickup_entry = PickupData.objects.filter(text=random_line).first()
                if analytics_entry and pickup_entry:
                    PickupAnalytics.objects.create(analytics = analytics_entry, pickup_data = pickup_entry, count = 1)
            return Response(random_line, content_type='application/json', status=status.HTTP_201_CREATED)

#This is working
class MostViewedbyAll(APIView):
    def get(self, request):
        most_viewed_line, count = self.find_most_viewed_pickup_line()
        return Response(f"The most viewed pickup line by all devices is '{most_viewed_line}' with a count of {count}.")

    def find_most_viewed_pickup_line(self):
        #To find the most viewed pickup line by all devices first I will need to take a count of each pickup line by device
        #Let's understand this by an example
        #Let's say we have a line called Hello and it has been twice by device_id 1 , 2 ,3
        #Let's say we have a line called Hi and it has been viewed once by device id 1,2,3
        #As you can see this Hello has been viewed more times then Hi
        #So we will take a sum of count of that specific line and count the number of devices that highest number
        #The highest count for a line by as many number of devices will be the most viewed line by all

        pickup_line_counts = (
            PickupAnalytics.objects
            .values('pickup_data__text')
            .annotate(total_count = Sum('count'))
            .order_by('-total_count')
        )

        highest_count = 0
        most_viewed_pickup_line = 0
        num_devices = 0

        for pickup_line_count in pickup_line_counts:
            count = pickup_line_count['total_count']
            num_devices_with_count = (
                PickupAnalytics.objects.filter(pickup_data__text = pickup_line_count['pickup_data__text'], count = count)
                .values('analytics__device_id')
                .distinct()
                .count()
            )

            if count > highest_count or (count == highest_count and num_devices_with_count > num_devices):
                highest_count = count
                most_viewed_pickup_line = pickup_line_count['pickup_data__text']
                num_devices = num_devices_with_count
                return most_viewed_pickup_line, highest_count


class MostViewedbyDevice(APIView):

    def get(self,request):
        most_viewed_by_device = self.find_most_viewed_pickup_line_by_device()
        response_data = []

        for device_id, data in most_viewed_by_device.items():
            pickup_line = data['pickup_line']
            count = data['count']
            response_data.append({
                'device_id': device_id,
                'pickup_line': pickup_line,
                'count': count
            })

        return Response(response_data)

    def find_most_viewed_pickup_line_by_device(self):
        device_pickup_lines = (
            PickupAnalytics.objects
            .values('analytics__device_id', 'pickup_data__text')
            .annotate(max_count=Max('count'))
        )

        most_viewed_by_device = {}

        for record in device_pickup_lines:
            device_id = record['analytics__device_id']
            pickup_line = record['pickup_data__text']
            count = record['max_count']

            if device_id in most_viewed_by_device:
                if count > most_viewed_by_device[device_id]['count']:
                    most_viewed_by_device[device_id] = {'Pickup Line': pickup_line, 'Count': count}
            else:
                most_viewed_by_device[device_id] = {'Pickup Line': pickup_line, 'Count': count}

        return most_viewed_by_device




