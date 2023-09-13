from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
import os
import random
from django.http import HttpResponse

class WallpaperView(APIView):

    def get(self, request, *args, **kwargs):
        # Define a dictionary to map category names to their corresponding directory paths.
        category_paths = {
            'anime': 'C:\\Users\\sweta\\Desktop\\externalapiproject\\pictures\\images\\anime',
            'ipl': 'C:\\Users\\sweta\\Desktop\\externalapiproject\\pictures\\images\\ipl',
            'f1': 'C:\\Users\\sweta\\Desktop\\externalapiproject\\pictures\\images\\f1',
            'nba': 'C:\\Users\\sweta\\Desktop\\externalapiproject\\pictures\\images\\nba',
        }
        category = kwargs['category']
        print(kwargs)

        # Check if the requested category is valid.
        if category not in category_paths:
            return HttpResponse("Invalid category", status=400)

        # Get the directory path for the requested category.
        image_dir = category_paths[category]

        try:
            image_files = os.listdir(image_dir)

            if not image_files:
                return HttpResponse(f"No images found in the {category} category", status=404)

            random_image = random.choice(image_files)
            image_path = os.path.join(image_dir, random_image)

            with open(image_path, "rb") as image_file:
                # Adjust the content type based on the image format (e.g., 'image/jpeg' for JPEG images).
                content_type = "image/jpeg"  # You may need to determine the correct content type.
                response = HttpResponse(image_file.read(), content_type=content_type)
                return response
        except FileNotFoundError:
            return HttpResponse(f"No images found in the {category} category", status=404)


    def post(self, request):
        DeviceNameModel = request.data.get('Device Name Model')
        SystemVersion = request.data.get('System Version')
        DeviceId = request.data.get('DeviceId')
        WidgetFamily = request.data.get('WidgetFamily')
        image_instance = Image(DeviceNameModel=DeviceNameModel, SystemVersion=SystemVersion, DeviceId=DeviceId, WidgetFamily=WidgetFamily)
        image_instance.save()

        response_data = {
            'Device Name Model': DeviceNameModel,
            'System Version': SystemVersion,
            'Device Id': DeviceId,
            'Widget Family': WidgetFamily,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


