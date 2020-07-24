# Generated by Django 3.0.6 on 2020-07-24 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0013_auto_20200624_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='address',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='collecting_date',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='detail_address',
        ),
        migrations.AddField(
            model_name='transaction',
            name='collecting_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Collecting datetime'),
        ),
    ]