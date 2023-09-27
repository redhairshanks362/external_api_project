import random

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from trio._tests.test_dtls import endpoint

# Create your views here.
from externalapiproject.settings import TV_SHOW_URL
from tvshow.models import TVShow
from tvshow.serializers import TVShowSerializers
from django.urls import reverse, get_script_prefix


class fetchQuotesWithLimit(APIView):
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
        #else:
        #This is working but when I add a random show name it shows 3 from whatever tv show is available in the db
        #Also for short part it is not showing me anything specific for short=false
        #Not working



    def post(self, request):
        DeviceNameModel = request.data.get('Device Name Model')
        SystemVersion = request.data.get('System Version')
        DeviceId = request.data.get('DeviceId')
        WidgetFamily = request.data.get('WidgetFamily')
        image_instance = TVShow(DeviceNameModel=DeviceNameModel, SystemVersion=SystemVersion, DeviceId=DeviceId, WidgetFamily=WidgetFamily)
        image_instance.save()

        response_data = {
            'Device Name Model': DeviceNameModel,
            'System Version': SystemVersion,
            'Device Id': DeviceId,
            'Widget Family': WidgetFamily,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class fetchQuotes(APIView):
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