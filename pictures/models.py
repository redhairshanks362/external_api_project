from django.db import models

# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=255)
    image_data = models.BinaryField()

