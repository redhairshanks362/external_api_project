from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from pickup.views import Rizz
from .import views
from .views import Fetch, Analytics_UnitTest, GetNasa_UnitTest

from speedtest import views
#from speedtest.views import get_client_ip
#from speedtest.views import Demo
#from speedtest.views import get_geo_location
from speedtest.views import SpeedTestView


urlpatterns = [
    path('', Fetch.as_view()),
    path('getUnitTest/', GetNasa_UnitTest.as_view()),
    path('postUnitTest/', Analytics_UnitTest.as_view()),
    #path('rizz/', Rizz.as_view()),
    #path('ipad/', SpeedTestView.as_view(), name='ipaddress'),
    #path('geo/', views.getGeoLoc, name='geoloc'),
    #path('', Demo.as_view()),
    #path('speed_test/', speed_test, name='speed_test')
    #path('get_geo_location', get_geo_location()),
    #path('get_client_ip', get_client_ip()),
    #path('', Demo.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
