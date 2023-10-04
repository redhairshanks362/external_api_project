from django.db import models

# Create your models here.

class WordModel(models.Model):
    wordOfTheDayinHindi = models.TextField(max_length=50)
    wordOfTheDayinEnglish = models.TextField(max_length=50)
    wordOfTheDayinEnglish_Usage_Example = models.TextField(max_length=2000)
    wordOfTheDayinHindi_Usage_Example = models.TextField(max_length=2000)
    date = models.DateField()

