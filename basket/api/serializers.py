from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.api.serializers import ProductListSerializer
from products.models import Product


class BasketOverViewSerializer(serializers.Serializer):
    total_qty = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    total_price_without_discount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)


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
        