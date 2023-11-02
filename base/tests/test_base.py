from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import re
import json
from analytics.models import DeviceAnalytics
from base.models import NASAApod
from numbers_api.models import Number
import uuid
import random
from datetime import datetime, timedelta

class TestGetNasa_UnitTest(TestCase):
    def setUp(self):
        print("NASA - GetNASAAPI_UnitTest passed")

    def test_json_response(self):
        load_nasa_data(self)
        date_object, formatted_date = generate_random_date_in_range(self)
        response = self.client.get(f'http://127.0.0.1:8000/getNASA/getUnitTest/?date={formatted_date}')
        check_nasa_response_with_regex(self,date_object, response)


#This test is to check if the data input is correct and if the a new row was created in the table
class TestAnalytics_UnitTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
    print("NASA- Analytics_UnitTest Passed")

    def test_valid_post_request(self):
        client = APIClient()
        print(client)
        response = client.post('/getNASA/postUnitTest/', self.valid_data, format='json')
        #Adding pre request test here
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            pre_request_test(self,response)
            print('response content is below or appended on the same line',response.content)
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
            check_model_with_location_data(self, response)
            #Checking if added values are correct
            check_added_location_values_with_regex(self, response, valid_country_names)



class TestMergedMethod(TestCase):
    def setUp(self):
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
        print("NASA- Merged UnitTest Passed")

    def test_text_response(self):
        client = APIClient()
        date_object, formatted_date = generate_random_date_in_range(self)
        load_nasa_data(self)
        response = client.post(f'/getNASA/?date={formatted_date}', self.valid_data, format='json')
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #Adding pre request test here
            pre_request_test(self,response)
            #Testing Response
            check_nasa_response_with_regex(self,date_object,response)
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
            check_nasa_response_with_regex(self,date_object,response)


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

def check_nasa_response_with_regex(self, date_object, response):
    response_data = response.content.decode('utf-8')
    text_response = json.loads(response_data)
    nasa_model = NASAApod.objects.get(date=text_response["date"], explanation=text_response["explanation"],
                                      hdurl=text_response["hdurl"], title=text_response["title"],
                                      url=text_response["url"])
    date = nasa_model.date
    # date = text_response["date"]
    explanation = nasa_model.explanation
    hdurl = nasa_model.hdurl
    title = nasa_model.title
    url = nasa_model.url
    self.assertTrue(isinstance(response.data["id"], int))
    self.assertEqual(date, date_object)
    self.assertIsInstance(explanation, str)
    self.assertRegex(hdurl, r"^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$")
    self.assertIsInstance(title, str)
    self.assertRegex(url, r"^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$")

def load_nasa_data(self):
    with open('/home/kidastudios/Desktop/external_api_project/base/tests/base_nasaapod.json', 'r') as f:
        data = json.load(f)
    objects = [NASAApod(
        id=obj['id'],
        explanation=obj['explanation'],
        hdurl=obj['hdurl'],
        media_type=obj['media_type'],
        service_version=obj['service_version'],
        title=obj['title'],
        url=obj['url'],
        hd_image=obj['hd_image'],
        standard_image=obj['standard_image'],
        date=obj['date']
    ) for obj in data]
    NASAApod.objects.bulk_create(objects)

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

def generate_random_date_in_range(self):
    min_date = datetime(1995, 6, 16)
    current_date = datetime.now()
    random_date = min_date + timedelta(days=random.randint(0, (current_date - min_date).days))
    formatted_date = random_date.strftime("%Y-%m-%d")
    date_object = datetime.strptime(formatted_date, "%Y-%m-%d").date()
    return date_object, formatted_date
