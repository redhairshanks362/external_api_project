from random import choice

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.urls import reverse, get_script_prefix
from rest_framework import status
from rest_framework.response import Response

from numbers_api.models import Number
from numbers_api.serializers import NumberSerializer


# Create your views here.

class NumberAPI(APIView):
    def get(self, request,**kwargs):
        day = kwargs.get('day')
        month = kwargs.get('month')
        host = request.get_host()
        base_url = f"http://{host}{get_script_prefix()}"
        #base_url = 'http://127.0.0.1:8000/factoftheDay'

        # day = int(day_str)
        # month = int(month_str)

        # if month is None or day is None:
        #     return Response({"error": "Invalid month or date"}, status=status.HTTP_400_BAD_REQUEST)

        number_api_url = f"{base_url}/factoftheDay/{month}/{day}/date"

        if not (1 <= month <= 12) or not (1 <= day <= 31):
            return Response({"error": "Invalid month or date"}, status=status.HTTP_400_BAD_REQUEST)

        records = Number.objects.filter(month=month, day=day)
        if records:
            # Randomly select one record from the filtered queryset.
            fact_text = choice(records).fact_text
            #serializer = NumberSerializer(fact_text)
            return HttpResponse(fact_text, content_type="text/plain")
        else:
            return Response({"error": "Data for the given month and date does not exist"}, status=status.HTTP_404_NOT_FOUND)










