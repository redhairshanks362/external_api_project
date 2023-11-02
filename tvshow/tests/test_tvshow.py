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

from tvshow.models import TVShow
from tvshow.util import all_tv_shows


#There are mutiple unit test classes and methods inside the class so need to create a lot of test classes
#path('getUnitTest1/<str:quotes>/', fetchQuotes_UnitTest.as_view(), name='quotes'),
class TestfetchJustQuotes_UnitTest(TestCase):
    def setUp(self):
        print("TVShow - fetch Single Quote_UnitTest passed")

    def test_json_response(self):
        load_tv_show_data(self)
        number = random.randint(1, 10)
        show = random.choice(all_tv_shows)
        # short = random.choice(['True', 'False'])
        short = 'False'
        api_response = self.client.get('http://127.0.0.1:8000/getTVQuotes/getUnitTest1/quotes/')
        #response = json.loads(api_response)
        json_response = api_response.content.decode('utf-8')
        json_dict = json.loads(json_response)
        tv_show_model = TVShow.objects.filter(show=json_dict["show"],character=json_dict["character"],text=json_dict["text"]).first()
        #id = tv_show_model.id
        show = tv_show_model.show
        character = tv_show_model.character
        #short = tv_show_model.short
        text = tv_show_model.text
        #self.assertTrue(isinstance(json_response.data["id"], int))
        self.assertIn(show, all_tv_shows)
        self.assertIsInstance(character, str)
        self.assertIsInstance(text, str)

        '''
        Writing print errors 
        self.assertTrue(isinstance(response.data["id"], int), f"Expected 'id' to be an integer, but got {type(response.data['id'])}")
self.assertEqual(date, date_object, f"Expected date '{date}' but got '{date_object}'")
self.assertIsInstance(explanation, str, "Expected 'explanation' to be a string")
self.assertRegex(hdurl, r"^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$", f"Invalid 'hdurl': {hdurl}")
self.assertIsInstance(title, str, "Expected 'title' to be a string")
self.assertRegex(url, r"^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$", f"Invalid 'url': {url}")

        '''


#path('getUnitTest2/<str:quotes>/<int:number>', fetchQuotesWithLimit_UnitTest.as_view(), name='quotes-limit'),
class TestfetchJustQuotesLimit_UnitTest(TestCase):
    def setUp(self):
        print("TVShow - fetch Multiple Quote_UnitTest passed")

    def test_json_response(self):
        load_tv_show_data(self)
        number = random.randint(1, 10)
        show = random.choice(all_tv_shows)
        # short = random.choice(['True', 'False'])
        short = 'False'
        api_response = self.client.get(f'http://127.0.0.1:8000/getTVQuotes/getUnitTest2query/quotes/{number}')
        #response = json.loads(api_response)
        json_response = api_response.content.decode('utf-8')
        json_dict = json.loads(json_response)
        for item in json_dict:
            tv_show_model = TVShow.objects.filter(show=item["show"], character=item["character"], text=item["text"]).first()
        #id = tv_show_model.id
        show = tv_show_model.show
        character = tv_show_model.character
        #short = tv_show_model.short
        text = tv_show_model.text
        #self.assertTrue(isinstance(json_response.data["id"], int))
        self.assertIn(show, all_tv_shows)
        self.assertIsInstance(character, str)
        self.assertIsInstance(text, str)

#path('getUnitTest2query/<str:quotes>/<int:number>', fetchQuotesWithLimit_UnitTest.as_view(), name='quotes-query-limit'),
class TestfetchQuotesQueryLimit_UnitTest(TestCase):
    def setUp(self):
        print("TVShow - fetch Multiple Quote_UnitTest passed")

    def test_json_response(self):
        load_tv_show_data(self)
        number = random.randint(1, 10)
        show = random.choice(all_tv_shows)
        # short = random.choice(['True', 'False'])
        short = 'False'
        api_response = self.client.get(f'http://127.0.0.1:8000/getTVQuotes/getUnitTest2query/quotes/{number}?show={show}&short={short}')
        #response = json.loads(api_response)
        json_response = api_response.content.decode('utf-8')
        json_dict = json.loads(json_response)
        for item in json_dict:
            tv_show_model = TVShow.objects.filter(show=item["show"], character=item["character"], text=item["text"]).first()
        #id = tv_show_model.id
        show = tv_show_model.show
        character = tv_show_model.character
        #short = tv_show_model.short
        text = tv_show_model.text
        #self.assertTrue(isinstance(json_response.data["id"], int))
        self.assertIn(show, all_tv_shows)
        self.assertIsInstance(character, str)
        self.assertIsInstance(text, str)

#path('getUnitTest1/', fetchQuotes_UnitTest.as_view()),
class TestfetchQuotesQuery_UnitTest(TestCase):
    def setUp(self):
        print("TVShow - fetch Multiple Quote_UnitTest passed")

    def test_json_response(self):
        load_tv_show_data(self)
        number = random.randint(1, 10)
        show = random.choice(all_tv_shows)
        # short = random.choice(['True', 'False'])
        short = 'False'
        api_response = self.client.get(f'http://127.0.0.1:8000/getTVQuotes/getUnitTest1/quotes/?show={show}&short={short}')
        #response = json.loads(api_response)
        json_response = api_response.content.decode('utf-8')
        json_dict = json.loads(json_response)
        tv_show_model = TVShow.objects.filter(show=json_dict["show"],character=json_dict["character"],text=json_dict["text"]).first()
        #id = tv_show_model.id
        show = tv_show_model.show
        character = tv_show_model.character
        #short = tv_show_model.short
        text = tv_show_model.text
        #self.assertTrue(isinstance(json_response.data["id"], int))
        self.assertIn(show, all_tv_shows)
        self.assertIsInstance(character, str)
        self.assertIsInstance(text, str)

class TestAnalytics_UnitTest(TestCase):
    def setUp(self):
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
        print("TV Show - Analytics_UnitTest Passed")

    def test_valid_post_request(self):
        client = APIClient()
        print(client)
        response = client.post('/getTVQuotes/postUnitTest/', self.valid_data, format='json')
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #Adding pre request test here
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
            check_model_with_location_data(self,response)
            #Checking if added values are correct
            check_added_location_values_with_regex(self,response, valid_country_names)


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

def load_tv_show_data(self):
    with open('/home/kidastudios/Desktop/external_api_project/tvshow/tests/tvshow_tvshow.json', 'r') as f:
        data = json.load(f)
    objects = [TVShow(
        id=obj['id'],
        show=obj['show'],
        character=obj['character'],
        short=obj['short'],
        text=obj['text'],
    ) for obj in data]
    TVShow.objects.bulk_create(objects)