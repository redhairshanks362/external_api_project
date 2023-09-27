import random

from celery import shared_task
from rest_framework import request
from rest_framework.exceptions import ValidationError

from externalapiproject.settings import TV_SHOW_URL
import requests

from tvshow.models import TVShow
from tvshow.serializers import TVShowSerializers
from tvshow.util import all_tv_shows
from tvshow.serializers import AllTvShowsSerializer


'''
    There are a few variations we are going to need here 
    first is we will store everything from every show's name from https://quotes.alakhpc.com/quotes/shows
    which then we can use for query parameter in the url 
    short only has boolean either true or false so that will be handled byu external api url 
    
    Let's talk about endpoints we have 
    when we hit 
    1.✔️
    {base_url}/{quotes} we get a random tv show quote from any tv show,character 
    Note - This endpoint will be useful to store Character name's if we hit this on celery every 5 hours or so we can store
    all the names of the characters just the we are storing show names
    Also with this we will keep hitting this to store random quotes in db 
    This is an imp endpoint 
    
    2.✔️f"{base_url}/{quotes}/{number} - Max 10 are allowed so use that number only 
    THis is also an important endpoint with this I think the maximum limit is 9 quotes at a time in a response from random tv shows,characters
    THis will be faster to store the data into db 
    
    3.✔️{base_url}/{quotes}?show={show}&short={short}✔️
    As discussed in the first point we can use first 2 endpoints to store everything and keep task for this commented 
    after some time we can keep this also in the loop of tasks 
    short is boolean and show will be used from db to get quotes
    
    4. ✔️
    {base_url}/{quotes}/{number}?show={show}&short={short}
    
    Again this will be useful to store multiple quotes 
    
    
    2nd and 4th will be useful to store multiple quotes making process faster 
    we can stress on these two on celery tasks
    
    First step will be storing shows then maybe 2nd endpoint to store character names and obvisouly other things like text and show
    
    
    '''

    #Writing seperate Celery tasks

#This is working on celery
@shared_task
def fetch_and_save_quotes_query():
    api_url = TV_SHOW_URL
    if all_tv_shows:
        random_show = random.choice(all_tv_shows)
        random_short = random.choice(['true', 'false'])
        print('from quotes query - random_show',random_show)
        print('from quotes query - random short',random_short)
        quotes_query_url = f"{api_url}/quotes?show={random_show}&short={random_short}"
        print('from quotes query - quotes_query_url', quotes_query_url)
        response = requests.get(quotes_query_url)

        if response.status_code == 200:
            data = response.json()
            print('from quotes query -data',data)
            show_name = data.get('show')
            print('from quotes query -show_name',show_name)
            character = data.get('character')
            print('from quotes query -character', character)
            text = data.get('text')
            print('from quotes query -text', text)

            response_data = {'show':show_name, 'character':character , 'text': text, 'short': random_short}

            print('from quotes query - response data',response_data)

            try:
                serializer = TVShowSerializers(data=response_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except ValidationError as e:
                # return {"error": f"An error occurred:"}
                print(e.detail)

#This is working on celery
@shared_task
def fetch_and_save_random_quotes():
    api_url = TV_SHOW_URL
    quotes_url = f"{api_url}/quotes"
    try:
        response = requests.get(quotes_url)
        data = response.json()
        show_name = data.get('shows')
        character = data.get('character')
        text = data.get('text')

        response_data = {'show':show_name, 'character':character , 'text': text}

        serializer = TVShowSerializers(data=response_data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except ValidationError as e:
        #return {"error": f"An error occurred:"}
        pass

##This has over 10 quotes so need to write a for loop to save all responses
#This is working on celery
@shared_task
def fetch_and_save_maximum_quotes_at_once():
    api_url = TV_SHOW_URL
    number = 10
    quotes_limit_url = f"{api_url}/quotes/{number}"
    try:
        response = requests.get(quotes_limit_url)
        data_list = response.json()

        # Create a list to hold the data for multiple records
        response_data_list = []

        for data in data_list:
            show_name = data.get('show')
            character = data.get('character')
            text = data.get('text')

            # Create a dictionary for each record and append it to the list
            response_data = {'show': show_name, 'character': character, 'text': text}
            response_data_list.append(response_data)

        # Now, use the list to create and save multiple records using the serializer
        serializer = TVShowSerializers(data=response_data_list, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except ValidationError as e:
        # Handle the validation error here
        pass


#This has over 10 quotes so need to write a for loop to save all responses
#This is working on celery
@shared_task
def fetch_and_save_quotes_query_limit():
    api_url = TV_SHOW_URL
    number = 10

    if all_tv_shows:
        random_show = random.choice(all_tv_shows)

        random_short = random.choice(['true', 'false'])
        print('from quotes query limit- random_show',random_show)
        print('from quotes query limit- random short',random_short)

        quotes_query_url = f"{api_url}/quotes/{number}?show={random_show}&short={random_short}"
        print('from quotes query limit- quotes_query_url', quotes_query_url)
        response = requests.get(quotes_query_url)
    try:

        if response.status_code == 200:
            data_list = response.json()
            print('from quotes query limit-data',data_list)

            # Create a list to hold the data for multiple records
            response_data_list = []

            for data in data_list:
                show_name = data.get('show')
                print('from quotes query limit -show_name',show_name)
                character = data.get('character')
                print('from quotes query limit-character', character)
                text = data.get('text')
                print('from quotes query limit-text', text)

                # Create a dictionary for each record and append it to the list
                response_data = {'show': show_name, 'character': character, 'text': text, 'short': random_short}
                response_data_list.append(response_data)

                print('from quotes query limit - response data',response_data_list)

            # Now, use the list to create and save multiple records using the serializer
            serializer = TVShowSerializers(data=response_data_list, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    except ValidationError as e:
        print(e.detail)













