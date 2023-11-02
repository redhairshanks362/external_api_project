import random
import unittest
from datetime import date

from django.conf import settings
from django.test import TestCase
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status
import re
import json
from datetime import datetime, date

from analytics.models import DeviceAnalytics
from unittest import mock
from wordOfTheDay.models import WordModel
from wordOfTheDay.models import WordModel
import uuid


# Create your tests here.

class TestGetWordOftheDay_UnitTest(TestCase):

    def setUp(self):
        print("Word of the Day - GetWordOftheDay_UnitTest passed")

    def test_json_response(self):
        load_word_data(self)
        #Using JSON file need to check if we can import model and check if it works
        #To call the GET call here we can write
        json_response = self.client.get('http://127.0.0.1:8000/wordOftheDay/getUnitTest/', format="json")
        check_word_of_the_day_response_with_regex(self,json_response)

#This test is to check if the data input is correct and if the a new row was created in the table
class TestAnalytics_UnitTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])
    print("Word of the Day - Analytics_UnitTest Passed")

    def test_valid_post_request(self):
        client = APIClient()
        print(client)
        response = client.post('/wordOftheDay/postUnitTest/', self.valid_data, format='json')
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

#This below method is a unit test case for the analytics method create which gives a response and sends a post request
class TestMergedMethod(TestCase):
    def setUp(self):
        print("wordOfTheDay passed")
        self.client = APIClient()
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        with_request_body = self.valid_data = {"device_type": "iPhone","os_version": "ios 13","device_id": random_uuid_str,"widget_family": "medium"}
        empty_request_body = self.valid_data = {}
        self.valid_data = random.choice([with_request_body, empty_request_body])

    def test_text_response(self):
        client = APIClient()
        json_response = client.post('/wordOftheDay/', self.valid_data, format='json')
        if all(key in json_response.content.decode('utf-8') for key in ['device_type', 'os_version', 'device_id', 'widget_family']):
            #Adding pre request test here
            pre_request_test(self,json_response)
            load_word_data(self)
            check_word_of_the_day_response_with_regex(self,json_response)
            #Post request test
            # Check if the model is created with the expected data
            check_model_with_expected_data(self)
            #Checking if the added values are correct according to regex
            check_added_values_with_regex(self)
        elif all(key in json_response.content.decode('utf-8') for key in ['city', 'ip', 'country']):
            with open('/home/kidastudios/Desktop/external_api_project/countries.json','r') as f:
                data = json.load(f)

            valid_country_names = [country['name'] for country in data]
            #Post request test
            check_model_with_location_data(self,json_response)
            #Checking if added values are correct
            check_added_location_values_with_regex(self,json_response,valid_country_names)
            #Testing response
            load_word_data(self)
            check_word_of_the_day_response_with_regex(self,json_response)
            #Post request test
            # Check if the model is created with the expected data
            check_model_with_expected_data(self)
            #Checking if the added values are correct according to regex
            check_added_values_with_regex(self)


def pre_request_test(self, response):
    self.assertIsInstance(self.valid_data['device_type'], str)
    self.assertIsInstance(self.valid_data['os_version'], str)
    self.assertRegex(str(self.valid_data['device_id']),
                     r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    self.assertIsInstance(self.valid_data['widget_family'], str)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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

def check_word_of_the_day_response_with_regex(self, json_response):
    # json_response = client.post('/wordOftheDay/', self.valid_data, format='json')
    self.assertEqual(json_response['Content-Type'], 'application/json')
    self.assertTrue(isinstance(json_response.data["id"], int))
    self.assertRegex(json_response.data["wordOfTheDayinHindi"], r"[ऀ-ॿ]+$")
    self.assertRegex(json_response.data["wordOfTheDayinEnglish"], r"^[a-zA-Z]+$")
    self.assertEqual(json_response.data["date"], str(date.today()))
    word_model = WordModel.objects.get(wordOfTheDayinHindi=json_response.data['wordOfTheDayinHindi'],
                                       wordOfTheDayinEnglish=json_response.data['wordOfTheDayinEnglish'],
                                       wordOfTheDayinHindi_Usage_Example=json_response.data[
                                           'wordOfTheDayinHindi_Usage_Example'],
                                       wordOfTheDayinEnglish_Usage_Example=json_response.data[
                                           'wordOfTheDayinEnglish_Usage_Example'])
    wordOfTheDayinEnglish = word_model.wordOfTheDayinEnglish
    wordOfTheDayinHindi = word_model.wordOfTheDayinHindi
    wordOfTheDayinEnglish_Usage_Example = word_model.wordOfTheDayinEnglish_Usage_Example
    wordOfTheDayinHindi_Usage_Example = word_model.wordOfTheDayinHindi_Usage_Example
    # Two patterns for Hindi and english this will check whether hindi word is present in the hindi sentence and same applies for english
    patternHindi = r"\b" + re.escape(wordOfTheDayinHindi) + r"\b"
    patternEnglish = r"\b" + re.escape(wordOfTheDayinEnglish) + r"\b"
    self.assertRegex(wordOfTheDayinHindi_Usage_Example, patternHindi)
    self.assertRegex(wordOfTheDayinEnglish_Usage_Example, patternEnglish)
    self.assertEqual(json_response.status_code, status.HTTP_200_OK)


def load_word_data(self):
    with open('/home/kidastudios/Desktop/external_api_project/wordOfTheDay/tests/wordOfTheDay_wordmodel.json',
              'r') as f:
        data = json.load(f)
    objects = [WordModel(
        id=obj['id'],
        wordOfTheDayinHindi=obj['wordOfTheDayinHindi'],
        wordOfTheDayinEnglish=obj['wordOfTheDayinEnglish'],
        wordOfTheDayinEnglish_Usage_Example=obj['wordOfTheDayinEnglish_Usage_Example'],
        wordOfTheDayinHindi_Usage_Example=obj['wordOfTheDayinHindi_Usage_Example'],
        date=obj['date']
    ) for obj in data]
    WordModel.objects.bulk_create(objects)


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
