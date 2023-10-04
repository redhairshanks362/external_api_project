from __future__ import absolute_import, unicode_literals
import os


from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','externalapiproject.settings')


app = Celery('externalapiproject')
app.conf.enable_utc = False
app.conf.worker_prefetch_multiplier = 1

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

#Celery beat settings
app.conf.beat_schedule = {
'fetch_and_save_pickup_lines': {
        'task': 'pickup.tasks.fetch_and_save_pickup_lines',
        'schedule': crontab(hour='*/1',minute='15')
},
'initiate_web_scraping': {
        'task': 'wordOfTheDay.tasks.initiate_web_scraping',
        'schedule': crontab(hour='*/5')
},
'fetch_and_save_nasa_data' : {
        'task': 'base.tasks.fetch_and_save_nasa_data',
        'schedule': crontab(minute='*/5')
},
'fetch_and_save_date_specific_data':{
        'task': 'numbers_api.tasks.fetch_and_save_date_specific_data',
        'schedule': crontab(minute='*/10')
},
'fetch_and_save_quotes_query': {
        'task': 'tvshow.tasks.fetch_and_save_quotes_query',
        'schedule': crontab(minute='*/10')
},
'fetch_and_save_random_quotes': {
        'task': 'tvshow.tasks.fetch_and_save_random_quotes',
        #minute='*/30'
        'schedule': crontab(minute='*/2')
},
'fetch_and_save_maximum_quotes_at_once': {
        'task': 'tvshow.tasks.fetch_and_save_maximum_quotes_at_once',
        'schedule': crontab(minute='*/3')
},
'fetch_and_save_quotes_query_limit': {
        'task': 'tvshow.tasks.fetch_and_save_quotes_query_limit',
        'schedule': crontab(minute='*/8')
},
}

app.autodiscover_tasks()
