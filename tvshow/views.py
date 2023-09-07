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


class fetchQuotes(APIView):
    def get(self, request, **kwargs):
        api_url = TV_SHOW_URL
        quotes = kwargs.get('quotes')
        stats = kwargs.get('stats')
        shows = kwargs.get('shows')
        number = kwargs.get('number')
        show = request.query_params.get('show')
        short = request.query_params.get('short')
        get_quotes_url = f"{api_url}/{quotes}"
        get_quotes_limit_url = f"{api_url}/{quotes}/{number}"
        get_quotes_query_url = f"{api_url}/{quotes}?show={show}&short={short}"
        get_quotes_query_limit_url = f"{api_url}/{quotes}/{number}?show={show}&short={short}"
        response_text = None

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

        if response_text:
            try:
                tv_show = TVShow.objects.get(text=response_text)
                serializer = TVShowSerializers(tv_show)
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

        '''
        #quotes = kwargs.get('quotes')
        #stats = kwargs.get('stats')
        #shows = kwargs.get('shows')
        number = kwargs.get('number')
        print('number', number)

        # show = request.query_params.get('show')
        # short = request.query_params.get('short')
        #get_quotes_stats_url = f'{api_url}/{quotes}/{stats}'
        #get_quotes_show_url = f'{api_url}/{quotes}/{shows}'
        if number is None:
            get_specific_url = f'{api_url}/quotes'
            data = requests.get(get_specific_url)
            print(data)
            print(data.status_code)
            print(data.json())
        else:
            get_specific_url = f'{api_url}/quotes/{number}'
            data = requests.get(get_specific_url)
            print(data)
            print(data.status_code)
            print(data.json())
        # get_specific_with_limit_url = f'{api_url}/{quotes}/{number}?show={show}&short={short}'
        #print('get_quotes_stats_url',get_quotes_stats_url)
        #print('get_quotes_show_url',get_quotes_show_url)
        #print('get_specific_url',get_specific_url)
        #print('get_specific_with_limit_url',get_specific_with_limit_url)

        
        if quotes and stats:
            if not quotes or stats:
                return Response({"error": "Quotes or States Path parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
            get_quotes_stats_url = f'{api_url}/{quotes}/{stats}'
            response = requests.get(get_quotes_stats_url)
            data = response.json()
            print('data of get quotes stats', data)
        elif quotes and shows:
            if not quotes or shows:
                return Response({"error": "Quotes or States Path parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
            get_quotes_show_url = f'{api_url}/{quotes}/{shows}'
            response = requests.get(get_quotes_show_url)
            data = response.json()
            print('data of get quotes shows', data)
            shows_list = data.get('shows', [])
            shows_str = ', '.join(shows_list)
            '''
        #if text:
        # if endpoint in ['quotes-query', 'quotes-query-limit', 'quotes', 'quotes-limit']:
        #     try:
        #         tv_show = TVShow.objects.get(text=text)  # Assuming "text" is the unique field
        #         serializer = TVShowSerializers(tv_show)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     except TVShow.DoesNotExist:
        #
        #         if endpoint == 'quotes-query':
        #             #if not show or short:
        #             #return Response({"error": "Quotes or States Query parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        #             get_specific_url = f'{api_url}/{endpoint}?show={show}&short={short}'
        #             response = requests.get(get_specific_url)
        #             data = response.json()
        #             print('data of get specific', data)
        #         elif endpoint == 'quotes-query-limit':
        #             #if not number:
        #             #return Response({"error": "Number Path parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        #             get_specific_with_limit_url = f'{api_url}/{endpoint}?show={show}&short={short}'
        #             response = requests.get(get_specific_with_limit_url)
        #             data = response.json()
        #             print('data of get specific limit', data)
        #         elif endpoint == 'quotes':
        #             #if not quotes:
        #             #return Response({"error": "Quotes Path Parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        #             get_just_quotes_url = f'{api_url}/{endpoint}'
        #             response = requests.get(get_just_quotes_url)
        #             data = response.json()
        #             print('data', data)
        #         elif endpoint == 'quotes-limit':
        #             #if not quotes or number:
        #             #return Response({"error": "Quotes or Number Path parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        #             get_just_quotes_with_limit_url = f'{api_url}/{endpoint}/{number}'
        #             response = requests.get(get_just_quotes_with_limit_url)
        #             data = response.json()
        #             print('data', data)
        #         else:
        #             return Response({"error": "Invalid endpoint"}, status=status.HTTP_400_BAD_REQUEST)
        #         serializer = TVShowSerializers(data)
        #         if serializer.is_valid():
        #             tv_show = serializer.save()
        '''
        else:
            api_url = TV_SHOW_URL
            response = requests.get(api_url)
            data = response.json()
            print('just the data', data)
        '''
        #return Response('serializer.data', status=status.HTTP_200_OK)
        '''
        response = requests.get(api_url)
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
        #if url =
    '''

    '''
    def get_quotes_stats(self, url):
        #GET /quotes/stats
        response = requests.get(url)
        return response

    def get_quotes_show(self,url):
        # GET / quotes / shows
        response = requests.get(url)
        return response

    def get_specific(self,url):
        #GET /quotes?show={show}&short={short}
        response = requests.get(url)
        return response

    def get_specific_with_limit(self,url):
        #Max of number quotes at a time.
        response = requests.get(url)
        return response
    '''

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