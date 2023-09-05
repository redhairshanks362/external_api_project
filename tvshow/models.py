from django.db import models


# Create your models here.

class TVShow(models.Model):
    show = models.TextField(max_length=500)
    # stats = models.TextField(max_length=500)
    character = models.TextField(max_length=200)
    text = models.TextField(max_length=1000)
    # total = models.TextField(max_length=500)
    #number = models.TextField(max_length=500)
    # shows = models.TextField(max_length=200)
    # docs = models.TextField(max_length=200)
    # name = models.TextField(max_length=200)
    # quotes = models.TextField(max_length=300)

    def __str__(self):
        return self.show
