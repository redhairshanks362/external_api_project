from django.urls import path

from wordOfTheDay.views import wordOfTheDay, GetWordOftheDay_UnitTest, Analytics_UnitTest

urlpatterns = [
    path('', wordOfTheDay.as_view()),
    path('getUnitTest/', GetWordOftheDay_UnitTest.as_view()),
    path('postUnitTest/', Analytics_UnitTest.as_view()),
]