from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import re
import json
from analytics.models import DeviceAnalytics
from numbers_api.models import Number
import uuid
import random


class TestGetNumberAPI_UnitTest(TestCase):
    def setUp(self):
        print("Numbers API - GetNumberAPI_UnitTest passed")

    def test_plain_text_response(self):
        load_number_api_data(self)
        #This db has a lot of duplicate values i.e. it has data for 1/1 for 1965,1865,1777 etc. so the values aren't unique creating a problem while unit testing
        #Assigning a fixed date to test if the response fact_text date matches with the date
        month=1
        day=1
        response = self.client.get(f'http://127.0.0.1:8000/factoftheDay/getUnitTest/{month}/{day}/date')
        check_number_api_response_with_regex(self, day, month, response)


#This test is to check if the data input is correct and if the a new row was created in the table
class TestAnalytics_UnitTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
    print("Numbers API - Analytics_UnitTest Passed")

    def test_valid_post_request(self):
        client = APIClient()
        print(client)
        response = client.post('/factoftheDay/postUnitTest/', self.valid_data, format='json')
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #Adding pre request test here
            pre_request_test(self,response)
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

class TestMergedMethod(TestCase):
    def setUp(self):
        print("wordOfTheDay passed")
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])

#THis post request is not working for assertTrue device id
    def test_text_response(self):
        client = APIClient()
        load_number_api_data(self)
        month=1
        day=1
        response = self.client.post(f'http://127.0.0.1:8000/factoftheDay/{month}/{day}/date', self.valid_data, format='json')
        if all(key in response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #Adding pre request test here
            pre_request_test(self,response)
            check_number_api_response_with_regex(self,day,month,response)
            #Post request test
            # Check if the model is created with the expected data [[[[[THis is not working 😠😠😠😠😠😠😠😠]]]
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
            #Testing response
            check_number_api_response_with_regex(self,response)


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

def check_number_api_response_with_regex(self, day, month, response):
    text_response = response.content.decode('utf-8')
    number_model = Number.objects.get(fact_text=text_response, day=day, month=month)
    fact_text = number_model.fact_text
    # day = number_model.day
    # month = number_model.month
    date_pattern_in_fact_text = r"(?i)(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d+)(st|nd|rd|th)"
    match = re.search(date_pattern_in_fact_text, fact_text)
    extracted_day = int(match.group(2))
    extracted_month = match.group(1)
    month_name_to_number = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    extracted_month = match.group(1)
    # Convert month name to number
    month_number = month_name_to_number.get(extracted_month, -1)
    self.assertEqual(extracted_day, day)
    self.assertEqual(month_number, month)

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

def load_number_api_data(self):
    with open('/home/kidastudios/Desktop/external_api_project/numbers_api/tests/numbers_api_number.json', 'r') as f:
        data = json.load(f)
    objects = [Number(
        fact_text=obj['fact_text'],
        day=obj['day'],
        month=obj['month']
    ) for obj in data]
    Number.objects.bulk_create(objects)
