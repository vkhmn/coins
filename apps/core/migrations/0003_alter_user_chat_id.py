# Generated by Django 4.1.3 on 2022-11-06 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_coinuser_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chat_id',
            field=models.IntegerField(verbose_name='Идентификатор чата'),
        ),
    ]
