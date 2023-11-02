import random
import socket

import requests
from django.db import transaction
from django.shortcuts import render
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import DeviceAnalytics
# from trio._tests.test_dtls import endpoint

# Create your views here.
from externalapiproject.settings import TV_SHOW_URL
from tvshow.models import TVShow
from tvshow.serializers import TVShowSerializers
from django.urls import reverse, get_script_prefix
from django.http import JsonResponse


class fetchQuotesWithLimit(APIView):
    def post(self, request, *args,**kwargs):
        base_url = 'http://127.0.0.1:8000'
        #host = request.get_host()
        #base_url = f"http://{host}{get_script_prefix()}"
        quotes = kwargs.get('quotes')
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        device_type = request.data.get('device_type')
        os_version = request.data.get('os_version')
        device_id = request.data.get('device_id')
        widget_family = request.data.get('widget_family')
        get_quotes_limit_url = f"{base_url}/{quotes}/{number}"
        get_quotes_query_limit_url = f"{base_url}/{quotes}/{number}?show={show}&short={short}"
        response_text = None

        if device_type is not None and os_version is not None and device_id is not None and widget_family is not None:
            device_analytics = {
                'device_type' : device_type,
                'os_version' : os_version,
                'device_id' : device_id,
                'widget_family' : widget_family,
            }

            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
            #Working
            if show is None and short is None:
                number = kwargs.get('number')
                try:
                    number = int(number)
                except ValueError:
                    if number <= 0:
                        return Response({"error": "Number must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

                response_data_list = []

                # Loop to generate the specified number of responses
                for i in range(number):
                    print('i',i)
                    random_tv_show = random.choice(TVShow.objects.all())

                    response_data = {
                        "show": random_tv_show.show,
                        "character": random_tv_show.character,
                        "text": random_tv_show.text,
                    }
                    response_data_list.append(response_data)

                return Response(response_data_list, status=status.HTTP_200_OK)
            if get_quotes_query_limit_url:
                show = request.query_params.get('show')
                print('show', show)
                short = request.query_params.get('short')
                number = kwargs.get('number')
                if not show or not short:
                    return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    number = int(number)
                except ValueError:
                    return Response({"error": "Invalid 'number' parameter"}, status=status.HTTP_400_BAD_REQUEST)

                if number <= 0:
                    return Response({"error": "Invalid 'number' parameter, must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    quotes = TVShow.objects.filter(show=show, short=short)
                    if not quotes.exists():
                        return Response({"error": f"No quotes found for show='{show}' and short='{short}'"}, status=status.HTTP_404_NOT_FOUND)

                    # Randomly select 'number' quotes from the filtered queryset
                    selected_quotes = random.sample(list(quotes), number)

                    serializer = TVShowSerializers(selected_quotes, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except TVShow.DoesNotExist:
                    return Response({"error": "TV show does not exist"}, status=status.HTTP_404_NOT_FOUND)
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
            if show is None and short is None:
                number = kwargs.get('number')
                try:
                    number = int(number)
                except ValueError:
                    #H
                    if number <= 0:
                        return Response({"error": "Number must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

                response_data_list = []

                # Loop to generate the specified number of responses
                for i in range(number):
                    print('i',i)
                    random_tv_show = random.choice(TVShow.objects.all())

                    response_data = {
                        "show": random_tv_show.show,
                        "character": random_tv_show.character,
                        "text": random_tv_show.text,
                    }
                    response_data_list.append(response_data)

                return Response(response_data_list, status=status.HTTP_200_OK)
            if get_quotes_query_limit_url:
                show = request.query_params.get('show')
                print('show', show)
                short = request.query_params.get('short')
                number = kwargs.get('number')
                if not show or not short:
                    return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    number = int(number)
                except ValueError:
                    return Response({"error": "Invalid 'number' parameter"}, status=status.HTTP_400_BAD_REQUEST)

                if number <= 0:
                    return Response({"error": "Invalid 'number' parameter, must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    quotes = TVShow.objects.filter(show=show, short=short)
                    if not quotes.exists():
                        return Response({"error": f"No quotes found for show='{show}' and short='{short}'"}, status=status.HTTP_404_NOT_FOUND)

                    # Randomly select 'number' quotes from the filtered queryset
                    selected_quotes = random.sample(list(quotes), number)

                    serializer = TVShowSerializers(selected_quotes, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except TVShow.DoesNotExist:
                    return Response({"error": "TV show does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
        existing_device_id = DeviceAnalytics.objects.filter(device_id=device_id).first()
        with transaction.atomic():
            if existing_device_id:
                if existing_device_id.TvShowCount is not None:
                    existing_device_id.TvShowCount += 1
                    existing_device_id.save()
                else:
                    existing_device_id.TvShowCount = 1
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
                device_analytics = DeviceAnalytics(**device_analytics, TvShowCount = 1)
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



class fetchQuotes(APIView):
    def post(self, request, *args,**kwargs):
        #host = request.get_host()
        #base_url = f"http://{host}{get_script_prefix()}"
        base_url = 'http://127.0.0.1:8000'
        quotes = kwargs.get('quotes')
        print('quotes', quotes)
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        #number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        device_type = request.data.get('device_type')
        os_version = request.data.get('os_version')
        device_id = request.data.get('device_id')
        widget_family = request.data.get('widget_family')
        print(show, short)
        get_quotes_url = f"{base_url}/{quotes}"
        get_quotes_query_url = f"{base_url}/{quotes}?show={show}&short={short}"
        print(get_quotes_url, get_quotes_query_url)

        if device_type is not None and os_version is not None and device_id is not None and widget_family is not None:
            device_analytics = {
                'device_type' : device_type,
                'os_version' : os_version,
                'device_id' : device_id,
                'widget_family' : widget_family,
            }

            self.updateDeviceAnalytics(device_analytics, device_id, widget_family)
            #Working
            if short is None and show is None:
                print('kwargs',kwargs)
                print('args',args)
                random_tv_show = random.choice(TVShow.objects.all())

                # Prepare the response data with show, character, and text
                response_data = {
                    "show": random_tv_show.show,
                    "character": random_tv_show.character,
                    "text": random_tv_show.text,
                }

                return Response(response_data, status=status.HTTP_200_OK)
        #Working
            else:
                show = request.query_params.get('show')
                short = request.query_params.get('short')
                print(show, short)
                if not show or not short:
                    return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    # tv_show = TVShow.objects.get(show=show)
                    quotes = TVShow.objects.filter(show=show, short=short)
                    if quotes.exists():
                        random_quote = random.choice(quotes)
                        serializer = TVShowSerializers(random_quote)

                        return Response(serializer.data, status=status.HTTP_200_OK)

                except TVShow.DoesNotExist:
                    return Response({"error": "Data for the given show does not exist"}, status=status.HTTP_404_NOT_FOUND)

                except ValueError:
                    return Response({"error": "Invalid show or short value"}, status=status.HTTP_400_BAD_REQUEST)

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
            if short is None and show is None:
                print('kwargs',kwargs)
                print('args',args)
                random_tv_show = random.choice(TVShow.objects.all())

                # Prepare the response data with show, character, and text
                response_data = {
                    "show": random_tv_show.show,
                    "character": random_tv_show.character,
                    "text": random_tv_show.text,
                }

                return Response(response_data, status=status.HTTP_200_OK)
            #Working
            else:
                show = request.query_params.get('show')
                short = request.query_params.get('short')
                print(show, short)
                if not show or not short:
                    return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    # tv_show = TVShow.objects.get(show=show)
                    quotes = TVShow.objects.filter(show=show, short=short)
                    if quotes.exists():
                        random_quote = random.choice(quotes)
                        serializer = TVShowSerializers(random_quote)

                        return Response(serializer.data, status=status.HTTP_200_OK)

                except TVShow.DoesNotExist:
                    return Response({"error": "Data for the given show does not exist"}, status=status.HTTP_404_NOT_FOUND)

                except ValueError:
                    return Response({"error": "Invalid show or short value"}, status=status.HTTP_400_BAD_REQUEST)

    def updateDeviceAnalytics(self, device_analytics, device_id, widget_family):
        existing_device_id = DeviceAnalytics.objects.filter(device_id=device_id).first()
        with transaction.atomic():
            if existing_device_id:
                if existing_device_id.TvShowCount is not None:
                    existing_device_id.TvShowCount += 1
                    existing_device_id.save()
                else:
                    existing_device_id.TvShowCount = 1
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
                device_analytics = DeviceAnalytics(**device_analytics, TvShowCount = 1)
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


#Making classes for unit Testing
class fetchQuotesWithLimit_UnitTestnotworking(APIView):
    def get(self, request, *args,**kwargs):
        base_url = 'http://127.0.0.1:8000'
        #host = request.get_host()
        #base_url = f"http://{host}{get_script_prefix()}"
        #This will retrieve the port and url at which it is running
        #base_url = reverse('home')
        quotes = kwargs.get('quotes')
        stats = kwargs.get('stats')
        shows = kwargs.get('shows')
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        get_quotes_url = f"{base_url}/{quotes}"
        get_quotes_limit_url = f"{base_url}/{quotes}/{number}"
        get_quotes_query_url = f"{base_url}/{quotes}?show={show}&short={short}"
        get_quotes_query_limit_url = f"{base_url}/{quotes}/{number}?show={show}&short={short}"
        get_quotes_limit_url = f"{base_url}/{quotes}/{number}"
        get_quotes_query_limit_url = f"{base_url}/{quotes}/{number}?show={show}&short={short}"
        response_text = None
        #Working
        if show is None and short is None:
            number = kwargs.get('number')
            try:
                number = int(number)
            except ValueError:
                if number <= 0:
                    return Response({"error": "Number must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

            response_data_list = []

            # Loop to generate the specified number of responses
            for i in range(number):
                print('i',i)
                random_tv_show = random.choice(TVShow.objects.all())

                response_data = {
                    "show": random_tv_show.show,
                    "character": random_tv_show.character,
                    "text": random_tv_show.text,
                }
                response_data_list.append(response_data)

        if get_quotes_url:
            response = requests.get(get_quotes_url)
            data = response.json()
            response_text = data.get('text')
        elif get_quotes_limit_url:
            response = requests.get(get_quotes_limit_url)
            data = response.json()
            response_text = data.get('text')
        elif get_quotes_query_url:
            response = requests.get(get_quotes_query_url)
            data = response.json()
            response_text = data.get('text')
        elif get_quotes_query_limit_url:
            response = requests.get(get_quotes_query_limit_url)
            data = response.json()
            response_text = data.get('text')
        else:
            return Response({"error": "Invalid endpoint"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(response_data_list, status=status.HTTP_200_OK)
        if get_quotes_query_limit_url:
            show = request.query_params.get('show')
            print('show', show)
            short = request.query_params.get('short')
            number = kwargs.get('number')
            if not show or not short:
                return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                number = int(number)
            except ValueError:
                return Response({"error": "Invalid 'number' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        if response_text:
            if number <= 0:
                return Response({"error": "Invalid 'number' parameter, must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                tv_show = TVShow.objects.get(text=response_text)
                serializer = TVShowSerializers(tv_show)
                quotes = TVShow.objects.filter(show=show, short=short)
                if not quotes.exists():
                    return Response({"error": f"No quotes found for show='{show}' and short='{short}'"}, status=status.HTTP_404_NOT_FOUND)

                # Randomly select 'number' quotes from the filtered queryset
                selected_quotes = random.sample(list(quotes), number)

                serializer = TVShowSerializers(selected_quotes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TVShow.DoesNotExist:
                serializer = TVShowSerializers(data=data)
                if serializer.is_valid():
                    tv_show = serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid response from the external API"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid endpoint2"}, status=status.HTTP_400_BAD_REQUEST)


class fetchQuotesWithLimit_UnitTest(APIView):
    def get(self, request, *args,**kwargs):
        #base_url = 'http://127.0.0.1:8000'
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
        #This will retrieve the port and url at which it is running
        #base_url = reverse('home')
        quotes = kwargs.get('quotes')
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        get_quotes_limit_url = f"{base_url}/{quotes}/{number}"
        get_quotes_query_limit_url = f"{base_url}/{quotes}/{number}?show={show}&short={short}"
        response_text = None
        #Working
        if show is None and short is None:
            number = kwargs.get('number')
            try:
                number = int(number)
            except ValueError:
                if number <= 0:
                    return Response({"error": "Number must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

            response_data_list = []

            # Loop to generate the specified number of responses
            for i in range(number):
                print('i',i)
                random_tv_show = random.choice(TVShow.objects.all())

                response_data = {
                    "show": random_tv_show.show,
                    "character": random_tv_show.character,
                    "text": random_tv_show.text,
                }
                response_data_list.append(response_data)

            return Response(response_data_list, status=status.HTTP_200_OK)
        if get_quotes_query_limit_url:
            show = request.query_params.get('show')
            print('show', show)
            short = request.query_params.get('short')
            number = kwargs.get('number')
            if not show or not short:
                return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                number = int(number)
            except ValueError:
                return Response({"error": "Invalid 'number' parameter"}, status=status.HTTP_400_BAD_REQUEST)

            if number <= 0:
                return Response({"error": "Invalid 'number' parameter, must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                quotes = TVShow.objects.filter(show=show, short=short)
                if not quotes.exists():
                    return Response({"error": f"No quotes found for show='{show}' and short='{short}'"}, status=status.HTTP_404_NOT_FOUND)

                # Randomly select 'number' quotes from the filtered queryset
                selected_quotes = random.sample(list(quotes), number)

                serializer = TVShowSerializers(selected_quotes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TVShow.DoesNotExist:
                return Response({"error": "TV show does not exist"}, status=status.HTTP_404_NOT_FOUND)


class fetchQuotes_UnitTestnotworking(APIView):
    def get(self, request, *args,**kwargs):
        #host = request.get_host()
        #base_url = f"http://{host}{get_script_prefix()}"
        base_url = 'http://127.0.0.1:8000'
        #This will retrieve the port and url at which it is running
        #base_url = reverse('home')
        quotes = kwargs.get('quotes')
        print('quotes', quotes)
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        #number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        print(show, short)
        get_quotes_url = f"{base_url}/{quotes}"
        get_quotes_query_url = f"{base_url}/{quotes}?show={show}&short={short}"
        print(get_quotes_url, get_quotes_query_url)
        #Working
        if short is None and show is None:
            print('kwargs',kwargs)
            print('args',args)
            random_tv_show = random.choice(TVShow.objects.all())

            # Prepare the response data with show, character, and text
            response_data = {
                "show": random_tv_show.show,
                "character": random_tv_show.character,
                "text": random_tv_show.text,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        #Working
        else:
            show = request.query_params.get('show')
            short = request.query_params.get('short')
            print(show, short)
            if not show or not short:
                return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # tv_show = TVShow.objects.get(show=show)
                quotes = TVShow.objects.filter(show=show, short=short).order_by('?')
                if quotes.exists():
                    random_quote = quotes.first()
                    #serializer = TVShowSerializers(random_quote.show, random_quote.character, random_quote.text, random_quote.id, random_quote.short)
                response_data = {
                        "show": random_quote.show,
                        "character": random_quote.character,
                        "text": random_quote.text,
                        "id": random_quote.id,
                        "short": random_quote.short,
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except TVShow.DoesNotExist:
                return Response({"error": "Data for the given show does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "Invalid show or short value"}, status=status.HTTP_400_BAD_REQUEST)

class fetchQuotes_UnitTest(APIView):
    def get(self, request, *args,**kwargs):
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
        #base_url = 'http://127.0.0.1:8000'
        #This will retrieve the port and url at which it is running
        #base_url = reverse('home')
        quotes = kwargs.get('quotes')
        print('quotes', quotes)
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        #number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        print(show, short)
        get_quotes_url = f"{base_url}/{quotes}"
        get_quotes_query_url = f"{base_url}/{quotes}?show={show}&short={short}"
        print(get_quotes_url, get_quotes_query_url)
        if short is None and show is None:
            print('kwargs',kwargs)
            print('args',args)
            random_tv_show = random.choice(TVShow.objects.all())

            # Prepare the response data with show, character, and text
            response_data = {
                "show": random_tv_show.show,
                "character": random_tv_show.character,
                "text": random_tv_show.text,
            }

            return Response(response_data, status=status.HTTP_200_OK)
            #Working
        else:
            show = request.query_params.get('show')
            short = request.query_params.get('short')
            print(show, short)
            if not show or not short:
                return Response({"error": "Both Show and short parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # tv_show = TVShow.objects.get(show=show)
                quotes = TVShow.objects.filter(show=show, short=short)
                if quotes.exists():
                    random_quote = random.choice(quotes)
                    serializer = TVShowSerializers(random_quote)

                    return Response(serializer.data, status=status.HTTP_200_OK)

            except TVShow.DoesNotExist:
                return Response({"error": "Data for the given show does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "Invalid show or short value"}, status=status.HTTP_400_BAD_REQUEST)


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
                if existing_device_id.TvShowCount is not None:
                    existing_device_id.TvShowCount += 1
                    existing_device_id.save()
                else:
                    existing_device_id.TvShowCount = 1
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
                device_analytics = DeviceAnalytics(**device_analytics, TvShowCount = 1)
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

