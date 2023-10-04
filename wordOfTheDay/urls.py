from django.urls import path

from wordOfTheDay.views import wordOfTheDay

urlpatterns = [
    path('', wordOfTheDay.as_view()),
    #H
]