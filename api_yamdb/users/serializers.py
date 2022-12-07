from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


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
        ],
        required=True,
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
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.filter(created_by_admin=False).all()
            )
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.filter(created_by_admin=False).all()
            )
        ],
        required=True,
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' запрещено"
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Обработчик токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()
