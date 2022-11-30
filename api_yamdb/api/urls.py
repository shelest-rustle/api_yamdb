from django.urls import path, include

from api.views import registration_user, get_token
from rest_framework import routers


urlpatterns = [
    path('v1/auth/signup/', registration_user, name='registration_user'),
    path('v1/auth/token/', get_token, name='get_token')
]
