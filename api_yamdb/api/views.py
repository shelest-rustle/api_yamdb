from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    UserReqistrationSerializer,
    TokenSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer
)
from api.permissions import IsAdminOrReadOnly
from titles.models import User, Title, Genre, Category


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    pass


@api_view(['POST'])
def registration_user(request):
    """Регистрирует юзера и отправляет письмо на email."""
    serializer = UserReqistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Yamdb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """
    Сравнивает код юзера с полученным
    в запросе кодом и выдает токен, если код совпадает.
    """
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirm_code = serializer.validated_data['confirmation_code']
    if default_token_generator.check_token(user, confirm_code):
        user_token = AccessToken.for_user(user)
        return Response({"token": str(user_token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GenreViewSet(CreateListDestroyViewSet):

    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre__name']

    def get_queryset(self):
        return Genre.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(CreateListDestroyViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__name']

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
