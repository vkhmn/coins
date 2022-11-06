from django.db import models
from mptt.models import TreeForeignKey

from apps.coins.models import Coin, Category


class Filter(models.Model):
    category = TreeForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='filters',
        verbose_name='Категория'
    )
    pattern = models.CharField('Паттерн', max_length=200)

    def __str__(self):
        return f'{self.category}: {self.pattern}'


class User(models.Model):
    email = models.EmailField(
        'Email',
        unique=True,
    )
    chat_id = models.IntegerField(
        'Идентификатор чата',
        unique=True,
    )
    filters = models.ManyToManyField(
        Filter,
        verbose_name='Паттерны',
    )
    coins = models.ManyToManyField(
        Coin,
        through='CoinUser',
        verbose_name='Монеты'
    )

    def __str__(self):
        return self.email


class Status(models.IntegerChoices):
    NEW = 0, 'Новое'
    SEND = 1, 'Отправлено'
    OLD = 2, 'Завешено'


class CoinUser(models.Model):
    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        verbose_name='Монета'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    message_id = models.IntegerField(
        'Индентификатор сообщения',
        blank=True,
        null=True
    )
    status = models.IntegerField(
        'Статус',
        choices=Status.choices,
        default=Status.NEW
    )

    def __str__(self):
        return f'{self.user} - {self.coin} - {self.status}'

    class Meta:
        unique_together = [['coin', 'user']]
