# Generated by Django 4.1 on 2022-08-11 11:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_voucher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voucher',
            old_name='on_time_use',
            new_name='one_time_use',
        ),
        migrations.AddField(
            model_name='voucher',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 11, 11, 47, 36, 130864, tzinfo=datetime.timezone.utc), verbose_name='valid voucher from'),
        ),
    ]
