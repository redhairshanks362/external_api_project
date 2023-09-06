import random

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from externalapiproject.settings import PICKUP_URL
from externalapiproject.settings import PICKUP2_URL
from pickup.models import PickupData

class Rizz(APIView):
    def get(self, request, **kwargs):
        api_url1 = PICKUP_URL
        api_url2 = PICKUP2_URL
        pickup1 = self.get_pickup_text(PICKUP_URL)
        pickup2 = self.get_pickup_json(PICKUP2_URL)

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

        all_the_pickup_lines = PickupData.objects.values_list('text', flat=True)
        random_line = random.choice(all_the_pickup_lines)

        return Response(random_line, content_type='text/plain', status=status.HTTP_200_OK)

    def get_pickup_text(self, url):
        response = requests.get(url)
        return response

    def get_pickup_json(self, url):
        response = requests.get(url)
        data = response.json()
        return data.get('pickup', '').strip()

