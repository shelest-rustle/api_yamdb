from django.urls import path, include

from rest_framework import routers

from api.views import registration_user, get_token, UserViewset


router_v1 = routers.DefaultRouter()

router_v1.register(r'users', UserViewset, basename='user')


urlpatterns = [
    path('v1/auth/signup/', registration_user, name='registration_user'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router_v1.urls)),
]
