# Generated by Django 2.2.28 on 2022-12-07 10:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScoredReview',
            new_name='Review',
        ),
    ]
