"""
URL configuration for externalapiproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tvshow.views import fetchQuotes

from speedtest import views
from numbers_api import urls
#from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getNASA/', include('base.urls')),
    path('speed_test/', include('speedtest.urls')),
    path('getPickup/', include('pickup.urls')),
    path('getTVQuotes/', include('tvshow.urls')),
    path('getUser/', include('user.urls')),
    path('wallpapers/', include('pictures.urls')),
    path('factoftheDay/', include('numbers_api.urls')),
    path('wordOftheDay/', include('wordOfTheDay.urls')),
    #path('', include('speedtest.urls')),
    #path('ipad/', views.ipaddress, name='ipaddress'),
    #path('geo/', views.getGeoLoc, name='geoloc'),
    #path('', include('speedtest.urls')),
]
