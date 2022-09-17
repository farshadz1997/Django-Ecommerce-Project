from .serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework import permissions
from rest_framework import viewsets
from django.urls import resolve

from ..models import Product


class ProductAPI(viewsets.ReadOnlyModelViewSet):
    """
    This view returns either list of products and their details.
    """
    queryset = Product.products.all()
    
    def get_serializer_class(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name == "api_product_detail":
            return ProductDetailSerializer
        return ProductListSerializer
    
    
class CategoryAPI(APIView):
    """
    List of all products filtered by category.
    """
    
    def get(self, request, *args, **kwargs):
        products = Product.products.filter(category__slug=self.kwargs["category"])
        serializer = ProductListSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class BrandAPI(APIView):
    """
    List of all products filtered by brand.
    """
    
    def get(self, request, *args, **kwargs):
        products = Product.products.filter(brand__slug=self.kwargs["brand"])
        serializer = ProductListSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class OnSaleAPI(APIView):
    """
    List of all products with discount.
    """
    
    def get(self, request, *args, **kwargs):
        products = Product.products.filter(discount__gt=0).order_by("-discount")
        serializer = ProductListSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class TopSellersAPI(APIView):
    """
    List of top 10 most sold products.
    """
    
    def get(self, request, *args, **kwargs):
        products = Product.products.filter(sold__gt=0).order_by("-sold")
        serializer = ProductListSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
    
class SearchAPI(APIView):
    """
    Return list of products filtered by search query.
    """
    
    def get(self, request, *args, **kwargs):
        products = Product.products.filter(title__icontains=self.request.data.get("query"))
        serializer = ProductListSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
    
class ProductListCreateAPI(generics.ListCreateAPIView):
    """
    API endpoint that allows products to be viewed or created by admins.
    """
    queryset = Product.products.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAdminUser]