# Generated by Django 4.1.3 on 2022-11-07 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_filter_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]