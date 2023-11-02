import socket

from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analytics.models import DeviceAnalytics
from wordOfTheDay import serializers
from wordOfTheDay.models import WordModel
from wordOfTheDay.serializers import WordSerializers
from datetime import datetime, date

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse


# Create your views here.
class wordOfTheDay(APIView):
    def post(self, request, **kwargs):
        #date_param = request.query_params.get('date')
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

            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)

            try:
                current_date = date.today()
                # current_date = '2023-10-21'
                date_string = str(current_date)
                valid_date = datetime.strptime(date_string, '%Y-%m-%d').date()

                if valid_date:

                    word_instance = WordModel.objects.get(date=valid_date)
                    serializer = WordSerializers(word_instance)

                # word_instance = WordModel.objects.get(id=43)
                # serializer = WordSerializers(word_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)
                #return Response(status=status.HTTP_200_OK)

            except WordModel.DoesNotExist:
                return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)

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

            try:
                current_date = date.today()
                #current_date = '2023-10-23'
                date_string = str(current_date)
                valid_date = datetime.strptime(date_string, '%Y-%m-%d').date()

                if valid_date:

                    word_instance = WordModel.objects.get(date=valid_date)
                    serializer = WordSerializers(word_instance)

                    return Response(serializer.data, status=status.HTTP_200_OK)

            except WordModel.DoesNotExist:
                return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
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
                device_analytics = DeviceAnalytics(**device_analytics, WordOftheDayCount = 1)
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

#Writing classes for unit tests here
class GetWordOftheDay_UnitTest(APIView):
    def get(self,*args,**kwargs):
        try:
            current_date = date.today()
            #current_date = '2023-11-02'
            date_string = str(current_date)
            valid_date = datetime.strptime(date_string, '%Y-%m-%d').date()

            if valid_date:

                word_instance = WordModel.objects.get(date=valid_date)
                serializer = WordSerializers(word_instance)

            # word_instance = WordModel.objects.get(id=43)
            # serializer = WordSerializers(word_instance)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except WordModel.DoesNotExist:
            return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)




class Analytics_UnitTest(APIView):
    def post(self, request):
        device_type = request.data.get('device_type')
        os_version = request.data.get('os_version')
        device_id = request.data.get('device_id')
        widget_family = request.data.get('widget_family')
        '''
        #Add these later
        #ISP = request.data.get('ISP')
        #Upload_Speed = request.data.get('Upload_Speed')
        #Ping = get_network_ping()
        #Server = request.data.get('Server')
        #ConnectionType = request.data.get('ConnectionType')
        #Add device id and widget family
        '''
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
                device_analytics = DeviceAnalytics(**device_analytics, WordOftheDayCount = 1)
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

