import random

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from externalapiproject.settings import PICKUP_URL
from externalapiproject.settings import PICKUP2_URL
from pickup.models import PickupData

# Create your views here.
class Rizz(APIView):
    def get(self, request, **kwargs):
        api_url1 = PICKUP_URL
        api_url2 = PICKUP2_URL

        '''
        if PickupData.objects.filter(text=pickup1).exists():
            pickup1_exists = True
        else:
            PickupData.objects.create(text=pickup1)
            pickup1_exists = False

        if PickupData.objects.filter(text=pickup2).exists():
            pickup2_exists = True
        else:
            PickupData.objects.create(text=pickup2)
            pickup2_exists = False
        '''
        # response_data = {
        #     'Pickup Line from JCWYT ': pickup1,
        #     'Pickup Line from VinuxD.Vercel': pickup2,
        # }
        #random_line = random.choice(pickup1)
        #Still need to add the random logic here
        all_the_pickup_lines = PickupData.objects.values_list('text', flat=True)
        random_line = random.choice(all_the_pickup_lines)
        if all_the_pickup_lines:
            response_data = random_line
        else:
            pickup1 = self.get_pickup_text(PICKUP_URL)
            pickup2 = self.get_pickup_json(PICKUP2_URL)
            if not PickupData.objects.filter(text=pickup1).exists():
                PickupData.objects.create(text=pickup1)

            if not PickupData.objects.filter(text=pickup2).exists():
                PickupData.objects.create(text=pickup2)

            response_data = {
             'Pickup Line from JCWYT ': pickup1,
             'Pickup Line from VinuxD.Vercel': pickup2,
            }

        return Response(response_data, content_type='text/plain', status=status.HTTP_200_OK)


        '''
        api_url1 = PICKUP_URL
        api_url2 = PICKUP_URL2
        print('api_url', api_url1)
        response = requests.get(api_url1)
        # data = response.json()
        print('data', response)
        print('status code', response.status_code)
        return Response(response, status=status.HTTP_200_OK)
        '''

    def get_pickup_text(self, url):
        response = requests.get(url)
        return response

    def get_pickup_json(self, url):
        response = requests.get(url)
        data = response.json()
        return data.get('pickup', '').strip()

