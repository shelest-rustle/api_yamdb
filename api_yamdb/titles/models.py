from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Наследованная модель юзера.
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
        'Почта',
        unique=True,
    )
    username = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        unique=True
    )
    bio = models.TextField('О себе',blank=True)
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLES,
        default=user
    )