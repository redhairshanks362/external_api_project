from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
import os
import random
from django.http import HttpResponse, JsonResponse


class WallpaperView(APIView):
    #Old working code
    '''
    def get(self, request, *args, **kwargs):
        # Define a dictionary to map category names to their corresponding directory paths.
        category_paths = {
            'anime': '/home/kidastudios/Desktop/external_api_project/pictures/images/anime',
            'ipl': '/home/kidastudios/Desktop/external_api_project/pictures/images/ipl',
            'f1': '/home/kidastudios/Desktop/external_api_project/pictures/images/f1',
            'nba': '/home/kidastudios/Desktop/external_api_project/pictures/images/nba',
        }
        category = kwargs['category']
        print(kwargs)

        # Check if the requested category is valid.
        if category not in category_paths:
            return HttpResponse("Invalid category", status=400)


        # Get the directory path for the requested category.
        image_dir = category_paths[category]
        #When I want to use category under teams like f1/Redbull then use this below code to enable
        # if category == 'f1':
        #     available_teams = ['Redbull', 'Ferrari', 'Mercedes']
        #     response_data = {
        #         'message': 'Choose one of these teams: Redbull, Ferrari, Mercedes and pass it in the path variable',
        #         'available_teams': available_teams
        #     }
        #     return JsonResponse(response_data)
        #
        # if category == 'nba':
        #     available_teams = ['Golden State Warriors', 'Houston Rockets', 'Los Angeles Lakers', 'Milwaukee Bucks']
        #     response_data = {
        #         'message': 'Choose one of these teams: Golden State Warriors, Houston Rockets, Los Angeles Lakers, Milwaukee Bucks and pass it in the path variable',
        #         'available_teams': available_teams
        #     }
        #     return JsonResponse(response_data)

        try:
            image_files = os.listdir(image_dir)

            if not image_files:
                return HttpResponse(f"No images found in the {category} category", status=404)

            random_image = random.choice(image_files)
            image_path = os.path.join(image_dir, random_image)

            with open(image_path, "rb") as image_file:
                content_type = "image/jpeg"
                response = HttpResponse(image_file.read(), content_type=content_type)
                return response
        except FileNotFoundError:
            return HttpResponse(f"No images found in the {category} category", status=404)
            '''
    def get(self, request, *args, **kwargs):

        category_paths = {
            'anime': '/home/kidastudios/Desktop/external_api_project/pictures/images/anime',
            'ipl': '/home/kidastudios/Desktop/external_api_project/pictures/images/ipl',
            'f1': '/home/kidastudios/Desktop/external_api_project/pictures/images/f1',
            'nba': '/home/kidastudios/Desktop/external_api_project/pictures/images/nba',
        }
        category = kwargs['category']
        print(kwargs)


        if category not in category_paths:
            return HttpResponse("Invalid category", status=400)


        image_dir = category_paths[category]

        if category == 'f1':
            f1_directory = '/home/kidastudios/Desktop/external_api_project/pictures/images/f1'
            team_folders = os.listdir(f1_directory)

            team_folders = [folder for folder in team_folders if os.path.isdir(os.path.join(f1_directory, folder))]

            if not team_folders:
                return HttpResponse("No F1 team folders found", status=404)

            random_team = random.choice(team_folders)
            team_directory = os.path.join(f1_directory, random_team)
            image_dir = team_directory

        elif category == 'nba':
            nba_directory = '/home/kidastudios/Desktop/external_api_project/pictures/images/nba'
            team_folders = os.listdir(nba_directory)

            team_folders = [folder for folder in team_folders if os.path.isdir(os.path.join(nba_directory, folder))]

            if not team_folders:
                return HttpResponse("No NBA team folders found", status=404)

            random_team = random.choice(team_folders)
            team_directory = os.path.join(nba_directory, random_team)
            image_dir = team_directory

        try:
            image_files = os.listdir(image_dir)

            if not image_files:
                return HttpResponse(f"No images found in the {category} category", status=404)

            random_image = random.choice(image_files)
            image_path = os.path.join(image_dir, random_image)

            with open(image_path, "rb") as image_file:
                content_type = "image/jpeg"
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

    #Extra working code
'''
class F1TeamView(APIView):
    #When we want to retrieve wallpapers for specific team use this below code
    
    def get(self, request,*args,**kwargs):
        team_paths = {
            'Redbull': '/home/kidastudios/Desktop/external_api_project/pictures/images/f1/Redbull',
            'Ferrari': '/home/kidastudios/Desktop/external_api_project/pictures/images/f1/Ferrari',
            'Mercedes': '/home/kidastudios/Desktop/external_api_project/pictures/images/f1/Mercedes',
        }
        team = kwargs['team']
        print(kwargs)

        if team not in team_paths:
            return HttpResponse("Team not available",status=400)

        #Get the directory path
        image_dir = team_paths[team]

        try:
            image_files = os.listdir(image_dir)

            if not image_files:
                return HttpResponse(f"No images found in the {team} team", status=404)

            random_image = random.choice(image_files)
            image_path = os.path.join(image_dir, random_image)

            with open(image_path, "rb") as image_file:
                content_type = "image/jpeg"
                response = HttpResponse(image_file.read(), content_type=content_type)
                return response
        except FileNotFoundError:
            return HttpResponse(f"No images found in the {team} team",status=404)
            
            
            def get(self,request,*args, **kwargs):
                f1_directory = '/home/kidastudios/Desktop/external_api_project/pictures/images/f1'
                team_folders = os.listdir(f1_directory)
        
                team_folders = [folder for folder in team_folders if os.path.isdir(os.path.join(f1_directory, folder))]
        
                if not team_folders:
                    return HttpResponse("No F1 team folders found", status=404)
        
                # random_team = random.choice(team_folders)
                # team_directory = os.path.join(f1_directory, random_team)
                # try:
                #     image_files = os.listdir(team_directory)
                # 
                #     if not image_files:
                #         return HttpResponse(f"No Images found in the {random_team} team folder", status=404)
                # 
                #     random_image = random.choice(image_files)
                #     image_path = os.path.join(team_directory, random_image)
        
                    with open(image_path, "rb") as image_file:
                        content_type = "image/jpeg"
                        response = HttpResponse(image_file.read(), content_type=content_type)
                        return response
                except FileNotFoundError:
                    return HttpResponse(f"No images found in the {random_team} team folder", status=404)

class NBATeamView(APIView):
    def get(self, request, *args, **kwargs):
        nba_directory = '/home/kidastudios/Desktop/external_api_project/pictures/images/nba'
        team_folders = os.listdir(nba_directory)

        # Remove any non-directory files from the list
        team_folders = [folder for folder in team_folders if os.path.isdir(os.path.join(nba_directory, folder))]

        if not team_folders:
            return HttpResponse("No NBA team folders found", status=404)

        random_team = random.choice(team_folders)
        team_directory = os.path.join(nba_directory, random_team)

        try:
            image_files = os.listdir(team_directory)

            if not image_files:
                return HttpResponse(f"No images found in the {random_team} team folder", status=404)

            random_image = random.choice(image_files)
            image_path = os.path.join(team_directory, random_image)

            with open(image_path, "rb") as image_file:
                content_type = "image/jpeg"
                response = HttpResponse(image_file.read(), content_type=content_type)
                return response
        except FileNotFoundError:
            return HttpResponse(f"No images found in the {random_team} team folder", status=404)

'''



