from rest_framework import serializers
from ..models import Product, Category, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image", "alt_text", "is_feature")


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.title
    
    def get_brand(self, obj):
        return obj.brand.title
    
    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.main_image[0].image.url
        return request.build_absolute_uri(image_url)
    
    class Meta:
        model = Product
        fields = ("id", "title", "quantity", "category", "brand", "discount", "final_price", "image")
        

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.title
    
    def get_brand(self, obj):
        return obj.brand.title
    
    class Meta:
        model = Product
        exclude = ("id", "slug", "created_at", "updated_at", "user_wishlist", "sold", "is_active")