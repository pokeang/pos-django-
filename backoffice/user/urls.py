from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user/<int:pk>', views.user_RUD, name="Update, delete, get user"),
    path('user', views.user_register, name="register user"),
    path('users', views.user_list, name="user list"),
    # path('roles', views.roles_list, name="list roles user")
    # path('login', obtain_auth_token, name="login"),
    path('login', views.login, name="login"),
    path('profile', views.profile, name="profile")
]
#