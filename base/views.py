import io
import socket

from PIL.Image import Image
from django.db import transaction
from django.shortcuts import render
from django.core.files.base import ContentFile
from PIL import Image
#from StringIO import StringIO

# Create your views here.
import requests
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analytics.models import DeviceAnalytics
from .models import NASAApod
from .serializers import ApodSerializer
from decouple import config
from externalapiproject.settings import NASA_API_KEY
from externalapiproject.settings import URL
from datetime import datetime,date
import os
import requests
#from speedtest.views import Fetch
#from speedtest.views import Demo
from django.http import JsonResponse

#H
class Fetch(APIView):
    throttle_scope = 'nasa'
    throttle_classes = (ScopedRateThrottle,)
    def post(self, request, **kwargs):
        '''
        date_param = request.query_params.get('date')  # Get the date from query parameter

        if not date_param:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            valid_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            minimum_date = date(1995, 6, 16)

            if valid_date < minimum_date:
                return Response({"error": "Date must be greater than Jun 16, 1995"}, status=status.HTTP_409_CONFLICT)

            apod_instance = NASAApod.objects.get(date=valid_date)
            serializer = ApodSerializer(apod_instance)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except NASAApod.DoesNotExist:
            return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)
            '''
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

            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)s

            if not date_param:
                return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                valid_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                minimum_date = date(1995, 6, 16)

                if valid_date < minimum_date:
                    return Response({"error": "Date must be greater than Jun 16, 1995"}, status=status.HTTP_409_CONFLICT)

                apod_instance = NASAApod.objects.get(date=valid_date)
                serializer = ApodSerializer(apod_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except NASAApod.DoesNotExist:
                return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

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

            if not date_param:
                return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                valid_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                minimum_date = date(1995, 6, 16)

                if valid_date < minimum_date:
                    return Response({"error": "Date must be greater than Jun 16, 1995"}, status=status.HTTP_409_CONFLICT)

                apod_instance = NASAApod.objects.get(date=valid_date)
                serializer = ApodSerializer(apod_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except NASAApod.DoesNotExist:
                return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
        existing_device_id = DeviceAnalytics.objects.filter(device_id=device_id).first()
        with transaction.atomic():
            if existing_device_id:
                if existing_device_id.NasaCount is not None:
                    existing_device_id.NasaCount += 1
                    existing_device_id.save()
                else:
                    existing_device_id.NasaCount = 1
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
                device_analytics = DeviceAnalytics(**device_analytics, NasaCount = 1)
                device_analytics.save()

    def save_images(self, date, hdurl, url):
        # Create a directory structure based on the date
        image_dir = os.path.join("static/images", date)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Generate unique filenames for the images
        hd_image_filename = os.path.join(image_dir, "hd_image.jpg")
        standard_image_filename = os.path.join(image_dir, "standard_image.jpg")

        # Download and save the HD image
        hd_response = requests.get(hdurl)
        if hd_response.status_code == 200:
            with open(hd_image_filename, "wb") as hd_file:
                hd_file.write(hd_response.content)

                # Resize the HD image
                hd_image = Image.open(hd_image_filename)
                hd_image = hd_image.resize((800, 800))
                hd_image.save(hd_image_filename)

        # Download and save the standard image
        response = requests.get(url)
        if response.status_code == 200:
            with open(standard_image_filename, "wb") as file:
                file.write(response.content)

                # Resize the standard image
                standard_image = Image.open(standard_image_filename)
                standard_image = standard_image.resize((800, 800))
                standard_image.save(standard_image_filename)

    '''
    def post(self, request):
        DeviceNameModel = request.data.get('Device Name Model')
        SystemVersion = request.data.get('System Version')
        DeviceId = request.data.get('DeviceId')
        WidgetFamily = request.data.get('WidgetFamily')
        image_instance = NASAApod(DeviceNameModel=DeviceNameModel, SystemVersion=SystemVersion, DeviceId=DeviceId, WidgetFamily=WidgetFamily)
        image_instance.save()

        response_data = {
            'Device Name Model': DeviceNameModel,
            'System Version': SystemVersion,
            'Device Id': DeviceId,
            'Widget Family': WidgetFamily,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    '''
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

class GetNasa_UnitTest(APIView):
    def get(self,request):
        date_param = request.query_params.get('date')  # Get the date from query parameter

        if not date_param:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            valid_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            minimum_date = date(1995, 6, 16)

            if valid_date < minimum_date:
                return Response({"error": "Date must be greater than Jun 16, 1995"}, status=status.HTTP_409_CONFLICT)

            apod_instance = NASAApod.objects.get(date=valid_date)
            serializer = ApodSerializer(apod_instance)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except NASAApod.DoesNotExist:
            return Response({"error": "Data for the given date does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)



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
                if existing_device_id.NasaCount is not None:
                    existing_device_id.NasaCount += 1
                    existing_device_id.save()
                else:
                    existing_device_id.NasaCount = 1
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
                device_analytics = DeviceAnalytics(**device_analytics, NasaCount = 1)
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