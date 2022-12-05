from django.urls import path, include

from rest_framework import routers

from .views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ScoredReviewViewSet,
    CommentViewSet
)
from users.views import registration_user, get_token, UserViewset
from rest_framework import routers

router_v1 = routers.DefaultRouter()


router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ScoredReviewViewSet, basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router_v1.register(r'users', UserViewset, basename='user')


urlpatterns = [
    path('v1/auth/signup/', registration_user, name='registration_user'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router_v1.urls))
]
