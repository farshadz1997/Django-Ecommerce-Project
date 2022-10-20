from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, When, Value, Case
from rest_framework import serializers

from products.api.serializers import ProductListSerializer
from products.models import Product
from orders.models import Voucher


class BasketOverViewSerializer(serializers.Serializer):
    total_qty = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    total_price_without_discount = serializers.SerializerMethodField(read_only=True)
    voucher = serializers.SerializerMethodField(required=False)
    discount = serializers.SerializerMethodField(read_only=True, default=0)
    
    def get_total_qty(self, obj):
        return len(obj)
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    
    def get_total_price_without_discount(self, obj):
        return obj.get_total_price_without_discount()
    
    def get_voucher(self, obj):
        return obj.voucher["code"]
    
    def get_discount(self, obj):
        return obj.voucher["discount"]

class BasketSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    qty = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], required=False, default=1)
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField(read_only=True)
    
    def get_total_price(self, obj):
        if obj.get("price", False):
            return round(Decimal(obj["price"]) * obj["qty"], 2)
        elif self.context["request"].method == "DELETE":
            return 0
        product = Product.products.get(id=obj["id"])
        return round(Decimal(product.final_price) * obj["qty"])
    
    def get_product(self, obj):
        product = get_object_or_404(Product, id=obj["id"])
        return ProductListSerializer(product, context={"request": self.context["request"]}).data
    
    def validate_qty(self, value):
        if Product.products.get(id=self.initial_data["id"]).quantity < value:
            raise serializers.ValidationError("Not enough in stock")
        return value
    
    
class VoucherSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10, required=True)
    
    def validate_code(self, voucher):
        code = Voucher.objects.filter(Q(max_use__gt=0) | Q(max_use=None),
                                        voucher_code__exact=voucher,
                                        is_active=True, 
                                        valid_from__lte=timezone.now(), 
                                        valid_until__gte=timezone.now())
        if code.exists():
            used_by_user = code.annotate(eligible=Case(
                When(one_time_use=True, then=Value(not code.filter(users=self.context["request"].user.id).exists())),
                When(one_time_use=False, then=Value(True)),
                default=Value(True)
                )).values('eligible')
            if used_by_user.first()['eligible']:
                return voucher
            else:
                raise serializers.ValidationError(_('You already used this promo code.'))
        else:
            raise serializers.ValidationError(_('Promo code is invalid'))
        