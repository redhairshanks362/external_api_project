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

# class ImageView(APIView):
#     def get(self, request, image_id):
#         try:
#             image = Image.objects.get(pk=image_id)
#         except Image.DoesNotExist:
#             return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = ImageSerializer(image)
#         return Response(serializer.data)

def get(request):
    image_dir = 'C:\\Users\\sweta\\Desktop\\externalapiproject\\pictures\\images'

    try:
        image_files = os.listdir(image_dir)

        if not image_files:
            return HttpResponse("No images found in the directory", status=404)


        random_image = random.choice(image_files)


        image_path = os.path.join(image_dir, random_image)


        with open(image_path, "rb") as image_file:
            response = HttpResponse(image_file.read(), content_type="image/jpeg")  # Adjust the content type as needed
            return response
    except FileNotFoundError:
        return HttpResponse("Image not found", status=404)


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


