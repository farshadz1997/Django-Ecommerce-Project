from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from ..basket import Basket
from .serializers import BasketOverViewSerializer, BasketSerializer


class BasketAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        data = [{"id":id, "qty": item["qty"], "price": item["price"],} for id, item in basket.basket.items()]
        serializer = BasketSerializer(data, many=True, context={"request": request})
        overview_serializer = self.get_basket_overview(request)
        return Response(
            {
                "basket": serializer.data,
                "overview": overview_serializer.data,
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
        overview_serializer = self.get_basket_overview(request)
        return Response(
        {
            "basket": serializer.data,
            "overview": overview_serializer.data,
        },
        status=status.HTTP_200_OK
        )
    
    def put(self, request, *args, **kwargs):
        basket = Basket(request)
        if request.data["id"] not in basket.basket.keys():
            return Response({"error": "Invalid item id provided"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BasketSerializer(data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        basket.update(request.data["id"], request.data["qty"])
        overview_serializer = self.get_basket_overview(request)
        return Response(
            {
                "basket": serializer.data,
                "overview": overview_serializer.data,
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, *args, **kwargs):
        basket = Basket(request)
        product_id = request.data.get("id")
        serializer = BasketSerializer(data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        basket.delete(product_id)
        overview_serializer = self.get_basket_overview(request)
        return Response(
        {
            "overview": overview_serializer.data,
        },)
    
    def get_basket_overview(self, request):
        basket = Basket(request)
        basket_overview = {
            "total_qty": len(basket),
            "total_price": basket.get_total_price(),
            "total_price_without_discount": basket.get_total_price_without_discount(),
        }
        overview_serializer = BasketOverViewSerializer(basket_overview)
        return overview_serializer