# Generated by Django 4.1.3 on 2022-12-08 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0002_rename_end_date_coin_time_end_coin_time_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='time_create',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата создания аукцина'),
        ),
    ]
