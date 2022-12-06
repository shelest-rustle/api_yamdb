from rest_framework import serializers

from titles.models import Title, Genre, Category, ScoredReview, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

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
