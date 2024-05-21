# Generated by Django 4.1 on 2022-08-12 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_voucher_voucher_code_alter_voucher_valid_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='max_use',
            field=models.PositiveIntegerField(blank=True, default=10, help_text='maximum number of times to use', verbose_name='maximum use (optional)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='voucher',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 12, 7, 31, 38, 393819, tzinfo=datetime.timezone.utc), verbose_name='valid voucher from'),
        ),
    ]
