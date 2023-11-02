from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from analytics.models import DeviceAnalytics


class TestWallpaperResponse(TestCase):
    def setUp(self):
        print("Response passed")

    def test_wallpaper_response(self):
        client = APIClient()
        response = client.get('/wallpapers/f1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestWallpaperResponse2(TestCase):
    def setUp(self):
        print("Response passed")

    def test_wallpaper_response(self):
        client = APIClient()
        response = client.get('/wallpapers/nba')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestWallpaperResponse3(TestCase):
    def setUp(self):
        print("Response passed")

    def test_wallpaper_response(self):
        client = APIClient()
        response = client.get('/wallpapers/ipl')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
