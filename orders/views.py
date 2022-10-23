from django.http.response import JsonResponse

from basket.basket import Basket

from .models import Order, OrderItem
from accounts.models import Address


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        address_id = request.POST.get('address_id')
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

        response = JsonResponse({'success': 'Order added',
                                 'add1': address.address_line_1,
                                 'add2': address.address_line_2,
                                 'city': address.city,
                                 'state': address.state,
                                 'country': address.country.code,
                                 'first_name': address.first_name,
                                 'last_name': address.last_name})
        return response


def payment_confirmation(data):
    obj = Order.objects.get(order_key=data)
    obj.billing_status = True
    obj.save()
    for item in obj.items.all():
        item.product.quantity -= item.quantity
        item.product.sold += item.quantity
        if item.product.quantity == 0:
            item.product.in_stock = False
        item.product.save()
        