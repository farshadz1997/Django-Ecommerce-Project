from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Voucher

from products.models import Product

from ..basket import Basket
from .serializers import BasketOverViewSerializer, BasketSerializer, VoucherSerializer


class BasketOverviewAPI(APIView):
    """
    This API is used to get the basket overview
    """

    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        serializer = BasketOverViewSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketDetailAPI(APIView):
    """
    This API is used to add, update and delete items from the basket.
    """
    
    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        data = [{"id":id, "qty": item["qty"], "price": item["price"],} for id, item in basket.basket.items()]
        serializer = BasketSerializer(data, many=True, context={"request": request})
        overview_serializer = BasketOverViewSerializer(basket)
        return Response(
            {
                "basket": serializer.data,
                "basket_overview": overview_serializer.data,
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        product_id = request.data.get("id")
        qty = request.data.get("qty")
        serializer = BasketSerializer(data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, id=product_id)
        basket.add(product, qty)
        overview_serializer = BasketOverViewSerializer(Basket(request))
        return Response(
        {
            "basket": serializer.data,
            "basket_overview": overview_serializer.data,
        },
        status=status.HTTP_200_OK
        )
    
    def put(self, request, *args, **kwargs):
        basket = Basket(request)
        if request.data["id"] not in basket.basket.keys():
            return Response({"error": "Invalid item id provided"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BasketSerializer(data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        basket.update(request.data["id"], request.data["qty"])
        overview_serializer = BasketOverViewSerializer(Basket(request))
        return Response(
            {
                "basket": serializer.data,
                "basket_overview": overview_serializer.data,
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, *args, **kwargs):
        basket = Basket(request)
        product_id = request.data.get("id")
        serializer = BasketSerializer(data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        basket.delete(product_id)
        overview_serializer = BasketOverViewSerializer(Basket(request))
        return Response(overview_serializer.data)
    
    
class VoucherAPI(APIView):
    """
    This API is used to add and remove promo codes from the basket.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        overview_serializer = BasketOverViewSerializer(Basket(request))
        return Response(overview_serializer.data)
        
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        serializer = VoucherSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        voucher = Voucher.objects.get(voucher_code=request.data["code"])
        basket.set_discount(voucher.voucher_code, voucher.discount)
        overview_serializer = BasketOverViewSerializer(basket)
        return Response(overview_serializer.data)
        
    def delete(self, request, *args, **kwargs):
        basket = Basket(request)
        basket.remove_discount()
        overview_serializer = BasketOverViewSerializer(basket)
        return Response(overview_serializer.data)