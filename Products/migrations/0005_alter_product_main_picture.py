# Generated by Django 3.2.4 on 2022-02-19 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_alter_product_main_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_picture',
            field=models.ImageField(upload_to='Products/', verbose_name='Main picture'),
        ),
    ]