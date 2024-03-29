from django.db.models import Prefetch
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from products.models import Product, ProductImage
from accounts.models import Address

class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().prefetch_related("items", Prefetch(
            "items__product__images", 
            ProductImage.objects.filter(is_feature=True), 
            "main_image"))


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='order_address', blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    phone = models.CharField(_("Phone Number"), max_length=20)
    address_line_1 = models.CharField(_('address line 1'), max_length=75)
    address_line_2 = models.CharField(_('address line 2'), max_length=75, blank=True, null=True)
    postcode = models.CharField(_("Postcode"), max_length=25)
    city = models.CharField(_('city'), max_length=50)
    state = models.CharField(_('state'), max_length=50)
    country = models.CharField(_('country'), max_length=50)
    delivery_instructions = models.TextField(_('delivery instructions'), max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_key = models.CharField(_('Order key'), max_length=200)
    billing_status = models.BooleanField(_('Billing status'), default=False)

    objects = models.Manager()
    orders = OrderManager()

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Voucher(models.Model):
    voucher_code = models.CharField(_('vocuher code'), max_length=10, unique=True, blank=False)
    discount = models.PositiveIntegerField(_('discount'), 
                                           help_text=_('how much discount set on the order'),
                                           validators=[MinValueValidator(1), MaxValueValidator(99)],
                                           blank=False,
                                           )
    one_time_use = models.BooleanField(_('one time use'), help_text=_('code can be used once for each user.'))
    max_use = models.PositiveIntegerField(_('maximum use (optional)'), help_text=_('maximum number of times to use'), blank=True)
    valid_from = models.DateTimeField(_('valid voucher from'), default=timezone.now)
    valid_until = models.DateTimeField(_('valid voucher until'))
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if (self.valid_from or self.valid_until) is None:
            raise ValidationError(_('You must provide date and time.'))
        if self.valid_from.date() > self.valid_until.date():
            raise ValidationError(_('Valid from must be set before valid until field'))
        if self.valid_from.date() == self.valid_until.date() and self.valid_from.time() > self.valid_until.time():
            raise ValidationError(_('Valid from time must be set before valid until time field'))
        super(Voucher, self).clean()
        
    def __str__(self):
        return f'{self.voucher_code} %{self.discount}'