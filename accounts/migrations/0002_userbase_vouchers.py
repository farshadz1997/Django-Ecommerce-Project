# Generated by Django 4.1 on 2022-08-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_voucher'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='vouchers',
            field=models.ManyToManyField(blank=True, related_name='users', to='orders.voucher'),
        ),
    ]
