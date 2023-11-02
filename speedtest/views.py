import socket
from django.db import transaction
from django.db.migrations import serializer
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework import status, response, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

#from speedtest import serializers
from django.core import serializers

from analytics.models import DeviceAnalytics
from speedtest.models import SpeedTest
from speedtest.serializers import STSerializers
import speedtest


# Create your views here.
'''
def get_client_ip(request):
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        ip = user_ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        #getGeoLoc(ip)
        # ipaddress(ip)
    # return HttpResponse("Welcome User!<br>You are visiting from: {}".format(ip))
    # speedtest_instance = SpeedTest.objects.get(ip)
    # data = response.json()
    # serializer = STSerializers(data=data)
    # if serializer.is_valid():
    # speedtest_instance = serializer.save()
    # return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return HttpResponse(ip)
    return ip

def get_network_ping():
    st = speedtest.SpeedTest()

    st.get_best_server()

    ping_time = st.results.ping
    return ping_time
'''



'''
@api_view(['GET'])
def ipaddress(request):
    ip = get_client_ip(request)
    speed = request.query_params.get('speed')
    datetime = request.query_params.get('datetime')
    #ipaddr = ipaddress(request)
    #ip_model_instance = SpeedTest.objects.get(ip=ip)
    ip_model_instance = SpeedTest(ip=ip)
    ip_model_instance.save()

    response_data = {
        'ip': ip,
        'speed': speed,
        'datetime': datetime,
    }

    return Response(response_data, status=status.HTTP_201_CREATED)\
'''
#H


class SpeedTestView(APIView):
    '''
    #Usually in java we used to write @GetMapping , @PostMapping , @PutMapping , @DeleteMapping
    #Over here whenever we use APIView library we can keep name of the function under class based view aqs post put and get this will be helpful for
    #platforms like postman to underdtand what are we doing
    #And in urls.py only the class based view is called its not like we have called each method over there
    '''
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

            #device_analytics_dict = self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)

        return JsonResponse(device_analytics, status=status.HTTP_201_CREATED)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
        existing_device_id = DeviceAnalytics.objects.filter(device_id=device_id).first()
        with transaction.atomic():
            if existing_device_id:
                if existing_device_id.SpeedTestCount is not None:
                    existing_device_id.SpeedTestCount += 1
                    existing_device_id.save()
                else:
                    existing_device_id.SpeedTestCount = 1
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
                device_analytics = DeviceAnalytics(**device_analytics, SpeedTestCount = 1)
                #device_analytics_dict = model_to_dict(device_analytics)
                device_analytics.save()
        return device_analytics

    def get(self, request):
        speedtest_instances = SpeedTest.objects.all()
        data = serializers.serialize('json', speedtest_instances)
        serializer = STSerializers(speedtest_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

"""
# def getGeoLoc(ipaddr, user):
    def getGeoLoc(self):
        # manually imported these lines inside here to make sure I just need to pass request
        # ipaddr = ipaddress(request)
        # userser = request.user
        ipaddr = get_client_ip(request)
        geoData = DbIpCity.get(ipaddr, api_key='free')
        ip = geoData.ip_address
        city = geoData.city
        country = geoData.country
        ip_model_instance = SpeedTest(ip=ip, city=city, country=country)
        ip_model_instance.save()
        response_data = {
            'ip': ip,
            'city': city,
            'country': country,
        }
        print(response_data)

        return HttpResponse({"message": "You check this out -", "data": response_data}, status=status.HTTP_200_OK)
"""