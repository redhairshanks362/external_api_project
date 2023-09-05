from django.urls import path

from pictures.views import get

urlpatterns = [
    path('image/', get,name='get_image'),
]