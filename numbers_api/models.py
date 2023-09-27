from django.db import models

# Create your models here.
class Number(models.Model):
    month = models.IntegerField()
    #date = models.IntegerField()
    fact_text = models.TextField(max_length=500)
    day = models.IntegerField()

    def __str__(self):
        return f"{self.month}/{self.day}"