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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Genre(models.Model):
    """
    Категории жанров.
    """

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Category(models.Model):
    """
    Категории (типы) произведений.
    """

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
    """

    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
