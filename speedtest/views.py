from django.shortcuts import render
from django.shortcuts import HttpResponse
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework import status, response, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from speedtest.models import SpeedTest
from speedtest.serializers import STSerializers
import speedtest


# Create your views here.

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


class SpeedTestView(APIView):
    #Usually in java we used to write @GetMapping , @PostMapping , @PutMapping , @DeleteMapping
    #Over here whenever we use APIView library we can keep name of the function under class based view aqs post put and get this will be helpful for
    #platforms like postman to underdtand what are we doing
    #And in urls.py only the class based view is called its not like we have called each method over there
    def post(self, request):
        ip = get_client_ip(request)
        Speed = request.data.get('Speed')
        DateTime = request.data.get('DateTime')
        BinaryUrl = request.data.get('BinaryUrl')
        DeviceNameModel = request.data.get('Device Name Model')
        SystemVersion = request.data.get('System Version')
        DeviceId = request.data.get('DeviceId')
        WidgetFamily = request.data.get('WidgetFamily')
        #Add these later
        #ISP = request.data.get('ISP')
        #Upload_Speed = request.data.get('Upload_Speed')
        #Ping = get_network_ping()
        #Server = request.data.get('Server')
        #ConnectionType = request.data.get('ConnectionType')
        #Add device id and widget family
        # ipaddr = ipaddress(request)
        # ip_model_instance = SpeedTest.objects.get(ip=ip)
        ip_model_instance = SpeedTest(ip=ip, Speed=Speed, DateTime=DateTime, BinaryUrl=BinaryUrl, DeviceNameModel=DeviceNameModel, SystemVersion=SystemVersion, DeviceId=DeviceId, WidgetFamily=WidgetFamily)
        ip_model_instance.save()

        response_data = {
            'Ip': ip,
            'Speed': Speed,
            'Date Time': DateTime,
            'Binary URL': BinaryUrl,
            'Device Name Model': DeviceNameModel,
            'System Version': SystemVersion,
            'Device Id': DeviceId,
            'Widget Family': WidgetFamily,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


    def get(self, request):
        speedtest_instances = SpeedTest.objects.all()
        data = []
        for instance in speedtest_instances:
            data.append({
                'Ip': instance.ip,
                'Speed': instance.Speed,
                'Date Time': instance.DateTime,
                'Binary Url': instance.BinaryUrl,
                'Device Name Model': instance.DeviceNameModel,
                'System Version': instance.SystemVersion,
                'Device Id': instance.DeviceId,
                'Widget Family': instance.WidgetFamily,
                #'ip_country': instance.ip_country,
                #'ip_city': instance.ip_city,
                #'url': instance.url,
            })
        return Response(data, status=status.HTTP_200_OK)

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