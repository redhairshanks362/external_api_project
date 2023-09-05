from django.core.files.base import ContentFile
from django.db import models
import os
import requests

# Create your models here.

def upload_image(instance, filename):
    # Construct the path for saving the images
    date = instance.date.strftime('%Y-%m-%d')
    subdir = os.path.join('images', date)
    return os.path.join(subdir, filename)

class NASAApod(models.Model):
    #copyright = models.CharField(null=True, max_length=200)
    date = models.DateField(auto_now_add=True)
    explanation = models.TextField(null=True,)

    hdurl = models.URLField()
    hd_image = models.ImageField(null=True)
    standard_image = models.ImageField(null=True)
    media_type = models.CharField(max_length=200)
    service_version = models.CharField(null=True,max_length=200)
    title = models.CharField(null=True,max_length=200)
    url = models.URLField(null=True,max_length=200)
    hd_image = models.ImageField(upload_to=upload_image, null=True)
    standard_image = models.ImageField(upload_to=upload_image, null=True)

    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super(NASAApod, self).save(*args, **kwargs)

        # Save the images using the provided URLs
        if self.hdurl:
            hd_image_content = requests.get(self.hdurl).content
            self.hd_image.save('hd_image.jpg', ContentFile(hd_image_content), save=False)

        if self.url:
            standard_image_content = requests.get(self.url).content
            self.standard_image.save('standard_image.jpg', ContentFile(standard_image_content), save=False)

    def __str__(self):
        return self.title


