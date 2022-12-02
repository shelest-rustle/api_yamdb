from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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
    bio = models.TextField('О себе', blank=True)
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
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).
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


class ScoredReview(models.Model):
    """
    Модель рецензии и рейтинга.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.CharField(max_length=1500)
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1.'),
            MaxValueValidator(10, 'Максимальная оценка - 10.')
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    help_text='Поставьте оценку от 1 до 10.'


class Comment(models.Model):
    """
    Модель комментария.
    """
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        ScoredReview,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    help_text='Добавьте комментарий.'