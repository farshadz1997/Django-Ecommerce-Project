from ..models import Order, OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from basket.basket import Basket
from accounts.models import Address
    

class CreateOrderAPI(APIView):
    """This API is used to create the order and add it to the database after payment."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        basket = Basket(request)
        order_key = request.data.get('order_key')
        address_id = request.data.get('address_id')
        address = Address.objects.get(customer=request.user, id=address_id)
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, address_id=address.pk,
                                        first_name=address.first_name, 
                                        last_name=address.last_name,
                                        address_line_1=address.address_line_1,
                                        address_line_2=address.address_line_2,
                                        city=address.city,
                                        state=address.state,
                                        country=address.country.name,
                                        phone=address.phone,
                                        postcode=address.postcode,
                                        total_paid=baskettotal,
                                        order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
        return Response({'success': 'Order added',
                        'add1': address.address_line_1,
                        'add2': address.address_line_2,
                        'city': address.city,
                        'state': address.state,
                        'country': address.country.code,
                        'first_name': address.first_name,
                        'last_name': address.last_name},
                        status=status.HTTP_201_CREATED)