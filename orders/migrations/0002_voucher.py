# Generated by Django 4.1 on 2022-08-11 11:35

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.PositiveIntegerField(help_text='how much discount set on the order', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='discount')),
                ('on_time_use', models.BooleanField(help_text='code can be used once for each use', verbose_name='one time use')),
                ('valid_from', models.DateTimeField(default=datetime.datetime(2022, 8, 11, 11, 34, 59, 746364, tzinfo=datetime.timezone.utc), verbose_name='valid voucher from')),
                ('valid_until', models.DateTimeField(verbose_name='valid voucher until')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
