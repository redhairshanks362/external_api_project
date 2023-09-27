from django.urls import path

from pictures.views import WallpaperView

urlpatterns = [
    #path('wallpapers/<str:category>/', get,name='get_image'),
    #path('wallpapers/', post, name='save_image_metadata'),
    path('<str:category>/', WallpaperView.as_view()),
    # path('f1/<str:team>/', F1TeamView.as_view(), name='f1_category_with_team'),
    # path('nba/<str:team>/', NBATeamView.as_view(), name='nba_category_with_team'),
    # path('wallpapers/<str:category>/', WallpaperView.as_view(), name='get_image'),
]