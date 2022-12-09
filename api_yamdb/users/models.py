from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Переопределенная модель юзера.
    """
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Имя',
        max_length=150,
        unique=True
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        """Декоратор для проверки, является ли админом юзер."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Декоратор для проверки, является ли модератором юзер."""
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['username']
