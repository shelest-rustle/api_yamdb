from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from titles.models import User


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


class UserReqistrationSerializer(serializers.ModelSerializer):
    """ Обработчик для регистрации юзеров."""

    class Meta:
        model = User   
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    """Обработчик токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def save(self):
        username = self.validated_data['username']
        confirmation_code = self.validated_data['confirmation_code']