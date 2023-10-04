from django.db import transaction
from django.shortcuts import render
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analytics.models import DeviceAnalytics
from wordOfTheDay import serializers
from wordOfTheDay.models import WordModel
from wordOfTheDay.serializers import WordSerializers
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# Create your views here.
class wordOfTheDay(APIView):
    def post(self, request, **kwargs):
        date_param = request.query_params.get('date')
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
                    if existing_device_id.WordOftheDayCount is not None:
                        existing_device_id.WordOftheDayCount += 1
                        existing_device_id.save()
                    else:
                        existing_device_id.WordOftheDayCount = 1
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

            if not date_param:
                return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                valid_date = datetime.strptime(date_param, '%Y-%m-%d').date()

                if valid_date:

                    word_instance = WordModel.objects.get(date=valid_date)
                    serializer = WordSerializers(word_instance)

                    return Response(serializer.data, status=status.HTTP_200_OK)

            except WordModel.DoesNotExist:
                return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)

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
            #H
            with transaction.atomic():
                if existing_device_id:
                    if existing_device_id.WordOftheDayCount is not None:
                        existing_device_id.WordOftheDayCount += 1
                        existing_device_id.save()
                    else:
                        existing_device_id.WordOftheDayCount = 1
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

            if not date_param:
                return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                valid_date = datetime.strptime(date_param, '%Y-%m-%d').date()

                if valid_date:

                    word_instance = WordModel.objects.get(date=valid_date)
                    serializer = WordSerializers(word_instance)

                    return Response(serializer.data, status=status.HTTP_200_OK)

            except WordModel.DoesNotExist:
                return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)
