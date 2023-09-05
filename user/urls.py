from django.urls import path

from user.views import user_profile, showall

from .views import create_user, user_profile
#from .views import get_user
#from .views import CreateProfileView

urlpatterns = [
    #path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    #path('admin/', admin.site.urls),
    #path('profile/<int:id>/', ProfileDetailView.as_view(), name='profile-detail'),
    #path('create-profile/', ProfileDetailView.as_view(), name='profile-detail'),
    #path('create-profile/', CreateProfileView.as_view(), name='create-profile'),
    path('users/', create_user, name='create_user'),
    path('show/', showall, name='show_all'),
    #path('users/<int:user_id>/', get_user, name='get_user'),
    path('users/<int:user_id>/', user_profile, name='get_user'),

]