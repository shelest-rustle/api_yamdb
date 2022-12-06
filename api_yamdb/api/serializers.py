from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from titles.models import Title, Genre, Category, ScoredReview, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )


class GenreSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """"""
    name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=Category.objects.all())
        ],
        required=True,
    )
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(queryset=Category.objects.all())
        ],
        required=True,
    )

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
            author=data.user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if not_first and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Обработчик комментариев."""
    author = serializers.StringRelatedField(read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
