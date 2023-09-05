from django.db import models

# Create your models here.

class SpeedTest(models.Model):
    #Check if something else can be used for internet speed
    #ip_address = models.TextField(null=True, max_length=400)
    #I want to add speed.description
    #DateTime
    Speed = models.TextField(null=True, max_length=400)
    DateTime = models.DateTimeField(auto_now_add=True)
    BinaryUrl = models.TextField(null=True,max_length=400)
    DeviceNameModel = models.TextField(null=True,max_length=400)
    SystemVersion = models.TextField(null=True,max_length=400)
    #DeviceId = models.TextField(null=True,max_length=200),
    #WidgetFamily = models.TextField(null=True,max_length=200),
    #Add whatever comes to mind check ookla speed test website and add things
    #isp , upload speed , ping , server , connections type - there is multi or check on gpt
    DeviceId = models.TextField(null=True, max_length=200)
    WidgetFamily = models.TextField(null=True, max_length=200)
    ISP = models.TextField(null=True, max_length=200)
    Upload_Speed = models.TextField(null=True, max_length=200)
    Ping = models.TextField(null=True, max_length=200)
    Server = models.TextField(null=True, max_length=200)
    ConnectionType = models.TextField(null=True,max_length=200)
    ip_country = models.CharField(max_length=200)
    ip_city = models.CharField(max_length=200)
    #ip = models.GenericIPAddressField(max_length=200)
    ip = models.GenericIPAddressField(null=True, default='127.0.0.1')
    url = models.URLField(null=True)


    # Widget_Family ((nullable=True) = Check acccess system families sent by sharan
    # so we will basically send this in post request body
