import io

from PIL.Image import Image
from django.shortcuts import render
from django.core.files.base import ContentFile
from PIL import Image
#from StringIO import StringIO

# Create your views here.
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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


class Fetch(APIView):
    def get(self, request, **kwargs):
        date = request.query_params.get('date')  # Get the date from query parameter
        print('Created at', date)
        if not date:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        #Adding validation for date the data on NASA API is between June 16 1995 to Aug 14 2023 (this date becomes current date so check functionallity
            valid_date = datetime.strptime(date, '%m/%d/%Y').date()
            minimum_date = date(1995, 6, 3)
            if valid_date > minimum_date:
                return Response({"success": "Date parameter is greater than minimum date"})
            else:
                return Response({"error" : "Date must be greater than Jun 16, 1995"}, status=status.HTTP_409_CONFLICT)
        #Check if data for this given data already exist in db
        try:
            #This below line is some what equal to GSPVO.getlompPk();
            apod_instance = NASAApod.objects.get(date=date)
            serializer = ApodSerializer(apod_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NASAApod.DoesNotExist:
            #This data is not present in the db so go ahead and call the API
            #pass

            api_key = NASA_API_KEY
            # url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
            base_url = URL
            print('APIKEY', api_key)
            print('Base Url', base_url)
            url = f'{base_url}?api_key={api_key}&date={date}'
            print('Final URl', url)
            '''
            api_key = 'cBNZnba1ktUVkqnXv1qrOfgfbWqM2XgvdEpwBc8e'
            url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}'
            '''

            response = requests.get(url)
            data = response.json()
            print('data', data)
            print('status code', response.status_code)
            if 'code' in data and data['code'] == 400:
                return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)

            hdurl = data.get('hdurl')
            url = data.get('url')

            self.save_images(date, hdurl, url)


            #To download and save the HD image
            # hd_image = self.download_and_resize_image(hdurl, (800, 800))
            # standard_image = self.download_and_resize_image(url, (800, 800))
            hd_image = "static/hd_image.jpg"
            image = "static/standard_image.jpg"
            #hd_image =
            serializer = ApodSerializer(data=data)
            if serializer.is_valid():
                apod_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def download_and_resize_image(self, image_url, size):
    #     response = requests.get(image_url)
    #     response.raise_for_status()
    #     image_data = response.content
    #
    #     image = Image.open(io.BytesIO(image_data))
    #     image = image.resize(size, Image.ANTIALIAS)
    #
    #     return image

    #

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

            # Resize the HD image to 800x800
            hd_image = Image.open(hd_image_filename)
            hd_image = hd_image.resize((800, 800), Image.ANTIALIAS)
            hd_image.save(hd_image_filename)

        # Download and save the standard image
        response = requests.get(url)
        if response.status_code == 200:
            with open(standard_image_filename, "wb") as file:
                file.write(response.content)

            # Resize the standard image to 800x800
            standard_image = Image.open(standard_image_filename)
            standard_image = standard_image.resize((800, 800), Image.ANTIALIAS)
            standard_image.save(standard_image_filename)




