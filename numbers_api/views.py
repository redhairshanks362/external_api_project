from random import choice

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework.views import APIView
from django.urls import reverse, get_script_prefix
from rest_framework import status
from rest_framework.response import Response

from analytics.models import DeviceAnalytics
from numbers_api.models import Number
from numbers_api.serializers import NumberSerializer


# Create your views here.

class NumberAPI(APIView):
    def post(self, request,**kwargs):
        day = kwargs.get('day')
        month = kwargs.get('month')
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
        device_type = request.data.get('device_type')
        os_version = request.data.get('os_version')
        device_id = request.data.get('device_id')
        widget_family = request.data.get('widget_family')
        #H

        number_api_url = f"{base_url}/factoftheDay/{month}/{day}/date"

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
                    if existing_device_id.FactofTheDayCount is not None:
                        existing_device_id.FactofTheDayCount += 1
                        existing_device_id.save()
                    else:
                        existing_device_id.FactofTheDayCount = 1
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

            if not (1 <= month <= 12) or not (1 <= day <= 31):
                return Response({"error": "Invalid month or date"}, status=status.HTTP_400_BAD_REQUEST)

            records = Number.objects.filter(month=month, day=day)
            if records:
                # Randomly select one record from the filtered queryset.
                fact_text = choice(records).fact_text
                #serializer = NumberSerializer(fact_text)
                return HttpResponse(fact_text, content_type="text/plain")
            else:
                return Response({"error": "Data for the given month and date does not exist"}, status=status.HTTP_404_NOT_FOUND)
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
                    if existing_device_id.FactofTheDayCount is not None:
                        existing_device_id.FactofTheDayCount += 1
                        existing_device_id.save()
                    else:
                        existing_device_id.FactofTheDayCount = 1
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
            if not (1 <= month <= 12) or not (1 <= day <= 31):
                return Response({"error": "Invalid month or date"}, status=status.HTTP_400_BAD_REQUEST)

            records = Number.objects.filter(month=month, day=day)
            if records:
                fact_text = choice(records).fact_text
                #serializer = NumberSerializer(fact_text)
                return HttpResponse(fact_text, content_type="text/plain")
            else:
                return Response({"error": "Data for the given month and date does not exist"}, status=status.HTTP_404_NOT_FOUND)













