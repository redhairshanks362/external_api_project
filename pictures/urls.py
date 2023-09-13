from django.urls import path

from pictures.views import WallpaperView


urlpatterns = [
    #path('wallpapers/<str:category>/', get,name='get_image'),
    #path('wallpapers/', post, name='save_image_metadata'),
    path('<str:category>/', WallpaperView.as_view()),
    # path('wallpapers/<str:category>/', WallpaperView.as_view(), name='get_image'),
]