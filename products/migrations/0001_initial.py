# Generated by Django 4.1 on 2022-08-06 13:03

import autoslug.fields
import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Ttile')),
                ('image', models.ImageField(help_text='Upload brand image or logo', upload_to='brands/', verbose_name='Image')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('sold', models.PositiveIntegerField(default=0, verbose_name='Sold')),
                ('regular_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)], verbose_name='Discount')),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Final price')),
                ('description', ckeditor.fields.RichTextField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('in_stock', models.BooleanField(default=True, verbose_name='Availability in stock')),
                ('is_active', models.BooleanField(default=True, verbose_name='Product visibility')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.brand', verbose_name='Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='Category')),
                ('user_wishlist', models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL, verbose_name='User wishlist')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-created_at'],
                'default_manager_name': 'products',
            },
            managers=[
                ('products', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProductTimestamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Time Stamp')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timestamps', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timestamps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(blank=True, help_text='Any special feature', max_length=50, null=True, verbose_name='Feature')),
                ('subtitle', models.CharField(blank=True, help_text='few detail', max_length=50, null=True, verbose_name='Subtitle')),
                ('image', models.ImageField(help_text='Upload a product image', upload_to='slider/', verbose_name='Slider image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Slider',
                'verbose_name_plural': 'Sliders',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload a product image', upload_to='products/', verbose_name='Image')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Product')),
            ],
        ),
    ]
