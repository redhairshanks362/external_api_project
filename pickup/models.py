from django.db import models

# Create your models here.

class PickupData(models.Model):
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text

