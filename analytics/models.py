from django.db import models

# Create your models here.
class DeviceAnalytics(models.Model):
    widgets = (
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large'),
        ('lockscreen', 'lockscreen'),
    )

    devices = (
        ('apple watch', 'apple watch'),
        ('iPhone', 'iPhone'),
        ('iPad', 'iPad'),
        ('mac','mac'),
    )

    device_id = models.UUIDField(null=True)
    widget_family = models.CharField(max_length=1000, null=True)
    device_type = models.TextField(null=True)
    os_version = models.CharField(max_length=20, null=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    city = models.CharField(default='city',max_length=50,null=True)
    country = models.CharField(max_length=50, null=True)
    PickupCount = models.IntegerField(null=True)
    NasaCount = models.IntegerField(null=True)
    FactofTheDayCount = models.IntegerField(null=True)
    SpeedTestCount = models.IntegerField(null=True)
    TvShowCount = models.IntegerField(null=True)
    WordOftheDayCount = models.IntegerField(null=True)


