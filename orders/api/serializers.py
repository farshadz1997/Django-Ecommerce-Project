from django.db.models import Sum
from rest_framework import serializers
from products.api.serializers import ProductListSerializer
from django.shortcuts import get_object_or_404
from ..models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    def get_product(self, obj):
        product = get_object_or_404(Product.products, id=obj.product.id)
        return ProductListSerializer(product, context={"request": self.context["request"]}).data

    class Meta:
        model = OrderItem
        exclude = ("order",)
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    total_qty = serializers.SerializerMethodField()
    items = OrderItemSerializer(read_only=True, many=True)

    def get_total_qty(self, obj):
        return obj.items.aggregate(total_qty=Sum("quantity"))["total_qty"]

    class Meta:
        model = Order
        exclude = ("id", "user", "billing_status", "order_key", "delivery_instructions", "created", "updated")
