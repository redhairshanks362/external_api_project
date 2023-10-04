import random

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


class fetchQuotesWithLimit(APIView):
    def post(self, request, *args,**kwargs):
        #base_url = 'http://127.0.0.1:8000'
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
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
                    device_analytics = DeviceAnalytics(**device_analytics)
                    device_analytics.save()
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

class fetchQuotes(APIView):
    def post(self, request, *args,**kwargs):
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
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
                    device_analytics = DeviceAnalytics(**device_analytics)
                    device_analytics.save()
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