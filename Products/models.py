from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active = True)

class Product(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    availability = models.BooleanField(_('Availability'), default=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    category = models.ForeignKey("Category", related_name='product', verbose_name = _('Category'), on_delete = models.CASCADE)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    description = RichTextField()
    slug = AutoSlugField(populate_from = 'title', unique = True)
    discount = models.PositiveIntegerField(_('Discount'), blank=True, null=True,
                                           validators = [MaxValueValidator(100), MinValueValidator(1)])
    main_picture = models.ImageField(_('Main picture'), upload_to = 'Products/')
    picture_2 = models.ImageField(_('Picture 2'), upload_to = 'Products/', blank=True, null=True)
    picture_3 = models.ImageField(_('Picture 3'), upload_to = 'Products/', blank=True, null=True)
    picture_4 = models.ImageField(_('Picture 4'), upload_to = 'Products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True, verbose_name='Availability in stock')
    is_active = models.BooleanField(default = True)
    objects = models.Manager()
    products = ProductManager()
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("Products:Product_detail", kwargs={"pk": self.pk, "slug": self.slug})
    
    def get_discount_price(self):
        if self.discount != None:
            return self.price - (self.price * self.discount / 100)
        return
    
class Category(models.Model):
    title = models.CharField(max_length = 255, unique = True)
    slug = AutoSlugField(populate_from = 'title')
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("Products:Product_category", kwargs={'category':self.slug})
    