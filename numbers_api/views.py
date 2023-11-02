import socket
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
from django.http import JsonResponse
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


        number_api_url = f"{base_url}/factoftheDay/{month}/{day}/date"

        if device_type is not None and os_version is not None and device_id is not None and widget_family is not None:
            device_analytics = {
                'device_type' : device_type,
                'os_version' : os_version,
                'device_id' : device_id,
                'widget_family' : widget_family,
            }

            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)

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
            client_ipv4 = self.get_client_ipv4(request)
            if client_ipv4:
                Location = DbIpCity.get(client_ipv4, api_key='free')
                city = Location.city
                country = Location.country
                device_analytics = {
                    'ip' : client_ipv4,
                    'city' : city,
                    'country' : country,
                }

            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
            if not (1 <= month <= 12) or not (1 <= day <= 31):
                return Response({"error": "Invalid month or date"}, status=status.HTTP_400_BAD_REQUEST)

            records = Number.objects.filter(month=month, day=day)
            if records:
                fact_text = choice(records).fact_text
                #serializer = NumberSerializer(fact_text)
                return HttpResponse(fact_text, content_type="text/plain")
            else:
                return Response({"error": "Data for the given month and date does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
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
                device_analytics = DeviceAnalytics(**device_analytics, FactofTheDayCount = 1)
                device_analytics.save()

    def get_client_ipv4(self,request):
        # Check the 'HTTP_X_FORWARDED_FOR' header for the client's IP address
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if forwarded_for:
            # The 'HTTP_X_FORWARDED_FOR' header can contain multiple IP addresses;
            # the client's address is typically the first one
            client_ip = forwarded_for.split(',')[0]
        else:
            # If 'HTTP_X_FORWARDED_FOR' is not available, fall back to 'REMOTE_ADDR'
            client_ip = request.META.get('REMOTE_ADDR')

        # Ensure the address is a valid IPv4 address
        try:
            socket.inet_pton(socket.AF_INET, client_ip)
            return client_ip
        except socket.error:
            # The address is not a valid IPv4 address
            return None


class GetNumberAPI_UnitTest(APIView):
    def get(self, request,**kwargs):
        day = kwargs.get('day')
        month = kwargs.get('month')
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
        #base_url = 'http://127.0.0.1:8000/factoftheDay'

        # day = int(day_str)
        # month = int(month_str)

        # if month is None or day is None:
        #     return Response({"error": "Invalid month or date"}, status=status.HTTP_400_BAD_REQUEST)

        number_api_url = f"{base_url}/factoftheDay/{month}/{day}/date"

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


class Analytics_UnitTest(APIView):
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

            #device_analytics_dict = self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
        else:
            #client_ipv4 = self.get_client_ipv4(request)
            #if client_ipv4:
            #Location = DbIpCity.get(client_ipv4, api_key='free')
            #city = Location.city
            city = 'Pune'
            #country = Location.country
            country = 'India'
            ip = '123.201.215.21'
            device_analytics = {
                'ip' : ip,
                'city' : city,
                'country' : country,
            }

            #device_analytics_dict = self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)

        return JsonResponse(device_analytics, status=status.HTTP_201_CREATED)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
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
                device_analytics = DeviceAnalytics(**device_analytics, FactofTheDayCount = 1)
                device_analytics.save()













