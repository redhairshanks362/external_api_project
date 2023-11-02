import json
import random

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from analytics.models import DeviceAnalytics
from pickup.models import PickupData
import uuid

class TestPickupLinesResponse(TestCase):
    def setUp(self):
        print("Response passed")

    def test_text_response(self):
        client = APIClient()
        #data = { 'text': "Are you Google Glass?{answer}'Cause you augment my reality." }
        #data = [{'text' : "Are you a time traveller coz I can see u in my future"}, {'text': "Are you Google Glass?{answer}'Cause you augment my reality."}]
        load_pickup_data(self)
        response = client.get('/getPickup/getUnitTest/')
        self.assertEqual(response['Content-Type'], 'application/json')
        print('Get Pickup',response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestPickupPost(TestCase):
    def setUp(self):
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
    print("Pickup - Analytics_UnitTest Passed")

    def test_valid_post_request(self):
        client = APIClient()
        print(client)
        response = client.post('/getPickup/postUnitTest/', self.valid_data, format='json')
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #Adding pre request test here
            pre_request_test(self,response)
            print('response content',response.content)
            #self.assertEqual(response.status_code, 200)
            print('response.status_code',response.status_code)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            #Post request test
            # Check if the model is created with the expected data
            check_model_with_expected_data(self)
            #Checking if the added values are correct according to regex
            check_added_values_with_regex(self)
        elif all(key in response.content.decode('utf-8') for key in ['city', 'ip', 'country']):
            with open('/home/kidastudios/Desktop/external_api_project/countries.json','r') as f:
                data = json.load(f)

            valid_country_names = [country['name'] for country in data]
            #Post request test
            check_model_with_location_data(self,response)
            #Checking if added values are correct
            check_added_location_values_with_regex(self,response,valid_country_names)

#This below method is a unit test case for the analytics method create which gives a response and sends a post request
class TestMergedMethod(TestCase):
    def setUp(self):
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
        print("Pickup - Merged UnitTest Passed")

    def test_text_response(self):
        client = APIClient()
        load_pickup_data(self)
        response = client.post('/getPickup/getRandomRizz/', self.valid_data, format='json')
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #data = { 'text': "Are you Google Glass?{answer}'Cause you augment my reality." }
            #data = [{'text' : "Are you a time traveller coz I can see u in my future"}, {'text': "Are you Google Glass?{answer}'Cause you augment my reality."}]
            #Adding pre request test here
            pre_request_test(self,response)
            #with open('pickup/pickup_pickupdata.json','r') as f:
            self.assertEqual(response['Content-Type'], 'application/json')
            print('Get Pickup',response.content)
            #Post request test
            # Check if the model is created with the expected data
            check_model_with_expected_data(self)
            #Checking if the added values are correct according to regex
            check_added_values_with_regex(self)
        elif all(key in response.content.decode('utf-8') for key in ['city', 'ip', 'country']):
            with open('/home/kidastudios/Desktop/external_api_project/countries.json','r') as f:
                data = json.load(f)

            valid_country_names = [country['name'] for country in data]
            #Post request test
            check_model_with_location_data(self, response)
            #Checking if added values are correct
            check_added_location_values_with_regex(self, response, valid_country_names)
            #Testing response
            self.assertEqual(response['Content-Type'], 'application/json')
            print('Get Pickup',response.content)


def pre_request_test(self, response):
    self.assertIsInstance(self.valid_data['device_type'], str)
    self.assertIsInstance(self.valid_data['os_version'], str)
    self.assertRegex(str(self.valid_data['device_id']),
                     r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    self.assertIsInstance(self.valid_data['widget_family'], str)

def check_model_with_expected_data(self):
    self.assertTrue(DeviceAnalytics.objects.filter(device_id=self.valid_data['device_id']).exists())
    self.assertTrue(DeviceAnalytics.objects.filter(device_type=self.valid_data['device_type']).exists())
    self.assertTrue(DeviceAnalytics.objects.filter(os_version=self.valid_data['os_version']).exists())
    self.assertTrue(DeviceAnalytics.objects.filter(widget_family=self.valid_data['widget_family']).exists())

def check_added_values_with_regex(self):
    device_analytics = DeviceAnalytics.objects.get(device_id=self.valid_data['device_id'],
                                                   device_type=self.valid_data['device_type'],
                                                   os_version=self.valid_data['os_version'],
                                                   widget_family=self.valid_data['widget_family'])
    device_id_str = str(device_analytics.device_id)
    device_type = device_analytics.device_type
    os_version = device_analytics.os_version
    widget_family = device_analytics.widget_family
    valid_options = ['medium', 'small', 'lockscreen', 'large']
    self.assertRegex(device_id_str, r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    self.assertIsInstance(device_type, str)
    self.assertIsInstance(os_version, str)
    self.assertIn(widget_family, valid_options)

def check_model_with_location_data(self, response):
    self.assertTrue(DeviceAnalytics.objects.filter(ip=json.loads(response.content.decode('utf-8'))['ip']).exists())
    self.assertTrue(
        DeviceAnalytics.objects.filter(city=json.loads(response.content.decode('utf-8'))['city']).exists())
    self.assertTrue(
        DeviceAnalytics.objects.filter(country=json.loads(response.content.decode('utf-8'))['country']).exists())

def check_added_location_values_with_regex(self, response, valid_country_names):
    self.assertIsInstance(json.loads(response.content.decode('utf-8'))['city'], str)
    self.assertRegex(json.loads(response.content.decode('utf-8'))['ip'], r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$')
    self.assertIn(json.loads(response.content.decode('utf-8'))['country'], valid_country_names)

def load_pickup_data(self):
    with open('/home/kidastudios/Desktop/external_api_project/pickup/pickup_pickupdata.json', 'r') as f:
        data = json.load(f)
    objects = [PickupData(text=obj['text']) for obj in data]
    PickupData.objects.bulk_create(objects)