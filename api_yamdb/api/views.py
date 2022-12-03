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
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, action, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    UserReqistrationSerializer,
    UserEditSeriializer,
    TokenSerializer,
    UserSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    ScoredReviewSerializer,
    CommentSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdmin
from titles.models import User, Title, Genre, Category, ScoredReview


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

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration_user(request):
    """Регистрирует юзера и отправляет письмо на email."""
    serializer = UserReqistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    User.objects.get_or_create(
        username = serializer.validated_data['username'],
        email = serializer.validated_data['email']
    )
    user = get_object_or_404(User, username=serializer.validated_data['username'])
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class UserViewset(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'get_self_profie':
            return UserEditSeriializer
        else:
            return UserSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return User.objects.all()
        else:
            return User.objects.filter(username=self.kwargs['pk'])

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def get_self_profie(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(User, username=self.kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(User, username=self.kwargs['pk'])
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

