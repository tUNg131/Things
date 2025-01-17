# Generated by Django 3.0.6 on 2020-06-16 14:59

import collect.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0007_auto_20200616_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicrecord',
            name='by_month',
            field=models.TextField(default=collect.models.Transaction_ObjectType.get_public_by_month, verbose_name='Public record grouped by month'),
        ),
        migrations.AlterField(
            model_name='publicrecord',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 59, 13, 349298, tzinfo=utc), verbose_name='Time added'),
        ),
    ]
