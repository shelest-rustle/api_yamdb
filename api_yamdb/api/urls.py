from django.urls import path, include
from rest_framework import routers

from .views import registration_user, get_token, TitleViewSet, CategoryViewSet, GenreViewSet


router_v1 = routers.DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/auth/signup/', registration_user, name='registration_user'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router_v1.urls))
]
