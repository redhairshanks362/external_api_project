from numbers_api.views import NumberAPI, GetNumberAPI_UnitTest, Analytics_UnitTest
from django.urls import path

urlpatterns = [
    path('<int:month>/<int:day>/date', NumberAPI.as_view()),
    path('getUnitTest/<int:month>/<int:day>/date', GetNumberAPI_UnitTest.as_view()),
    path('postUnitTest/', Analytics_UnitTest.as_view()),
]