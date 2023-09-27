from numbers_api.views import NumberAPI
from django.urls import path

urlpatterns = [
    #path('', Fetch.as_view()),
    path('<int:month>/<int:day>/date', NumberAPI.as_view()),
]