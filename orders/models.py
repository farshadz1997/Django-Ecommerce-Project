from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from Products.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(_('Full name'), max_length=50)
    address1 = models.CharField(_('Address 1'), max_length=250)
    address2 = models.CharField(_('Address 2'), max_length=250, blank=True)
    city = models.CharField(_('City'), max_length=100)
    phone = models.CharField(_('Phone number'), max_length=100)
    post_code = models.CharField(_('Post code'), max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_key = models.CharField(_('Order key'), max_length=200)
    billing_status = models.BooleanField(_('Billing status'), default=False)

    class Meta:
        ordering = ('-id', '-created')
    
    def __str__(self):
        return f'{self.id}. Ordered by {self.user.user_name}, on {self.date_created()}, total: ${self.total_paid}'
    
    def date_created(self):
        return str(self.created.strftime('%d/%m/%Y - %H:%M'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
