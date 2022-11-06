from django.core.management import BaseCommand

from apps.coins.models import Category
from apps.core.models import User, Filter


class Command(BaseCommand):
    """Django команда для заполнения базы данных."""

    def handle(self, *args, **options):
        user = User(
            chat_id=28535191,
            email='dj0n@mail.ru'
        )
        user.save()
        print('1')
        p1 = Category.objects.create(
            id=22,
            title='Монеты России до 1917 года'
        )
        p2 = Category.objects.create(
            id=23,
            title='Монеты СССР и России 1918 - 2022'
        )

        Category.objects.create(**{'id': 113, 'title': 'Серебро/Золото/Платина', 'parent': p1})
        Category.objects.create(**{'id': 114, 'title': 'Медь', 'parent': p1})
        Category.objects.create(**{'id': 116, 'title': 'Погодовка СССР', 'parent': p2})
        Category.objects.create(**{'id': 118, 'title': 'Погодовка Современная Россия', 'parent': p2})

        filters = [
            {'pattern': '1912', 'category_id': 113},
            {'pattern': '1912', 'category_id': 114},
            {'pattern': '2002', 'category_id': 118},
            {'pattern': '1921|1924|1925|1930|1931|1953|1983', 'category_id': 116},
        ]

        for f in filters:
            Filter.objects.create(**f)
