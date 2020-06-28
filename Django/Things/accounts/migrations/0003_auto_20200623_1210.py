# Generated by Django 3.0.6 on 2020-06-23 05:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200622_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Location'),
        ),
        migrations.AddField(
            model_name='user',
            name='detail_address',
            field=models.CharField(blank=True, help_text='Required for collections. 256 characters or fewer.', max_length=256, verbose_name='Detail address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined'),
        ),
    ]