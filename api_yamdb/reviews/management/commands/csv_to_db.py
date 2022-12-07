import csv

from django.core.management.base import BaseCommand

from titles.models import (
    Title,
    Genre,
    Category,
    ScoredReview,
    Comment
)
from users.models import User


CSV_PATH = 'static/data/'
FOREIGN_KEY_FIELDS = ('category', 'author')
DICT = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    ScoredReview: 'review.csv',
    Comment: 'comments.csv'
}


def csv_import(csv_data, model):
    objs = []
    for row in csv_data:
        for field in FOREIGN_KEY_FIELDS:
            if field in row:
                row[f'{field}_id'] = row[field]
                del row[field]
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'import data from csv files'

    def handle(self, *args, **kwargs):
        for model in DICT:
            with open(
                CSV_PATH + DICT[model],
                newline='',
                encoding='utf8'
            ) as csv_file:
                csv_import(csv.DictReader(csv_file), model)
        self.stdout.write(
            self.style.SUCCESS(
                'All csv rows loaded to database'
            )
        )
