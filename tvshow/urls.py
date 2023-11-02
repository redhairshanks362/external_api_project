from django.urls import path

#from pickup.views import Rizz
#from .import views
#from .views import Fetch

from speedtest import views
#from speedtest.views import get_client_ip
#from speedtest.views import Demo
#from speedtest.views import get_geo_location
from speedtest.views import SpeedTestView
from tvshow.views import fetchQuotes, fetchQuotesWithLimit, fetchQuotes_UnitTest, fetchQuotesWithLimit_UnitTest, \
    Analytics_UnitTest

urlpatterns = [
    path('', fetchQuotes.as_view()),
    #done
    path('postUnitTest/', Analytics_UnitTest.as_view()),
    #done
    path('getUnitTest1/', fetchQuotes_UnitTest.as_view()),
    #path('<str:quotes>/<str:stats>', fetchQuotes.as_view(), name='quotes-stats'),
    #path('<str:quotes>/<str:shows>', fetchQuotes.as_view(), name='quotes-shows'),
    #path('<str:quotes>/<int:number>', fetchQuotes.as_view(), name='quotes-limit'),
    #path('<str:quotes>/', fetchQuotes.as_view(), name='quotes-query')
    path('<str:quotes>/', fetchQuotes.as_view(), name='quotes'),
    #done
    path('getUnitTest1/<str:quotes>/', fetchQuotes_UnitTest.as_view(), name='quotes'),
    path('<str:quotes>/<int:number>', fetchQuotesWithLimit.as_view(), name='quotes-limit'),
    #done
    path('getUnitTest2/<str:quotes>/<int:number>', fetchQuotesWithLimit_UnitTest.as_view(), name='quotes-limit'),
    path('<str:quotes>/', fetchQuotes_UnitTest.as_view(), name='quotes-query'),
    path('<str:quotes>/<int:number>', fetchQuotesWithLimit.as_view(), name='quotes-query-limit'),
    #done
    path('getUnitTest2query/<str:quotes>/<int:number>', fetchQuotesWithLimit_UnitTest.as_view(), name='quotes-query-limit'),


    #  with query parameters
    # path('quotes/', fetchQuotes.as_view(), name='quotes'),
    # path('quotes/<int:number>', fetchQuotes.as_view(), name='quotes-limit'),
]