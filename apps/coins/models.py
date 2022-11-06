from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

ROOT_URL = 'https://coins.lave.ru/forum'


class Category(MPTTModel):
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='Родительская категория'
    )
    id = models.IntegerField(
        primary_key=True
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'id']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # def get_absolute_url(self):
    #    return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title


class Seller(models.Model):
    name = models.CharField('Пользователь', max_length=100)

    def __str__(self):
        return self.name


class Coin(models.Model):
    id = models.IntegerField(
        'Идентификатор монеты',
        unique=True,
        primary_key=True
    )
    category = TreeForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='coins',
        verbose_name='Категория'
    )
    title = models.CharField('Заголовок', max_length=100)
    image = models.URLField('Url изображения')
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        verbose_name='Продавец'
    )
    end_date = models.DateField(
        'Дата окончания аукциона',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    def to_msg(self):
        return f'*{self.category}*\n' \
           f'{self.title}\n' \
           f'{self.seller}\n' \
           f'{self.coin_url}'

    @property
    def coin_url(self):
        return f'{ROOT_URL}/viewtopic.php?f={self.category.id}&t={self.id}'
