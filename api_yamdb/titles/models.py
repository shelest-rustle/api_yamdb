from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Переопределенная модель юзера.
    """
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'
    ROLES = [
        (admin, 'Administrator'),
        (moderator, 'Moderator'),
        (user, 'User'),
    ]
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        unique=True
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLES,
        default=user
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        """Декоратор для проверки, является ли админом юзер."""
        if self.is_superuser:
            self.role = self.admin
            self.save()
        return self.role == self.admin

    @property
    def is_moderator(self):
        """Декоратор для проверки, является ли модератором юзер."""
        return self.role == self.moderator
