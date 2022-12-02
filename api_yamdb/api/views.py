from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.db.models.aggregates import Avg

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes


from api.serializers import (
    UserReqistrationSerializer,
    TokenSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    ScoredReviewSerializer,
    CommentSerializer
)
from api.permissions import IsAdminOrReadOnly
from titles.models import User, Title, Genre, Category, ScoredReview, Comment


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    pass


@api_view(['POST'])
@permission_classes([AllowAny]) 
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
@permission_classes([AllowAny])
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


@permission_classes([AllowAny])
class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GenreViewSet(CreateListDestroyViewSet):

    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre__name']

    def get_queryset(self):
        return Genre.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(CreateListDestroyViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__name']

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScoredReviewViewSet(viewsets.ModelViewSet):
    """Возвращает отзывы."""
    serializer_class = ScoredReviewSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Возвращает комментарии."""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(ScoredReview, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(ScoredReview, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
