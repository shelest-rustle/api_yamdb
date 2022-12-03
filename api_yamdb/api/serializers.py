from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from titles.models import User, Title, Genre, Category, ScoredReview, Comment


class UserSerializer(serializers.ModelSerializer):
    """Общий обработчик для юзера."""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class UserEditSeriializer(serializers.ModelSerializer):
    """Обаботчик для изменения данных юзером."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class UserReqistrationSerializer(serializers.Serializer):
    """ Обработчик для регистрации юзеров."""
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' запрещено"
            )
        return value

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']


class TokenSerializer(serializers.Serializer):
    """Обработчик токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def save(self):
        username = self.validated_data['username']
        confirmation_code = self.validated_data['confirmation_code']


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Category
        fields = '__all__'


class ScoredReviewSerializer(serializers.ModelSerializer):
    """Обработчик отзыва и рейтинга."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ScoredReview
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        not_first = ScoredReview.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if not_first and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Обработчик комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
