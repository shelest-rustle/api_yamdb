from django.db.models.aggregates import Avg

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import viewsets
from rest_framework.decorators import  permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    ScoredReviewSerializer,
    CommentSerializer
)
from .permissions import IsAdminOrReadOnly
from titles.models import Title, Genre, Category, ScoredReview

class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет, обрабатывающий GET, POST и DELETE запросы.
    """
    pass


@permission_classes([AllowAny])
class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет со всеми типами запросов для произведений.
    """

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GenreViewSet(CreateListDestroyViewSet):
    """
    Вьюсет для жанров, обрабатывающий запросы GET, POST и DELETE.
    """

    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre__name']

    def get_queryset(self):
        return Genre.objects.all()


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Вьюсет для категорий, обрабатывающий запросы
    GET, POST и DELETE.
    """

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
        review = get_object_or_404(
            ScoredReview, pk=self.kwargs.get("review_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(ScoredReview, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

