# Generated by Django 4.1.4 on 2023-01-25 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_user_unc_pattern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='pattern',
            field=models.CharField(max_length=1000, verbose_name='Паттерн'),
        ),
    ]
