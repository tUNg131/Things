# Generated by Django 3.0.6 on 2020-06-16 15:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0010_auto_20200616_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicrecord',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time added'),
        ),
    ]
