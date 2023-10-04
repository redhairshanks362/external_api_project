import time
from celery import shared_task
from rest_framework import serializers

from .models import WordModel
from .scrapers import scraper
from .serializers import WordSerializers

URL = "https://www.shabdkosh.com/word-of-the-day/english-hindi/"

@shared_task
def initiate_web_scraping():
    scraped_data = scraper(URL)
    #print('scraped data', scraped_data)
    existing_dates = WordModel.objects.values_list('date', flat=True)
    if scraped_data:
        date = scraped_data['date']
        if date in existing_dates:
            print(f"The word for {date} already exists in the database, skipping...")
        else:
            try:
                serializer = WordSerializers(data=scraped_data)
                if serializer.is_valid():
                    serializer.save()
                    print("Data saved")
            except serializers.ValidationError as e:
                print(e.detail)
