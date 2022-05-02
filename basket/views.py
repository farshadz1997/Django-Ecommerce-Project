from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from Products.models import Product
from .basket import Basket
import json

def basket_summary(request):
    basket = Basket(request)
    products = Product.objects.all().order_by('-pub_date')[:4]
    offers = Product.products.order_by('?')[:2]
    return render(request, 'basket/basket_summary.html', {'basket': basket, 'recent_products': products, 'offers': offers})

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        baskettottal = basket.get_total_price()
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty, 'subtotal': f"${baskettottal}"})
        return response
    
def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product = product_id)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': f"${baskettotal}"})
        return response

def basket_update(request):
    basket = Basket(request)
    products = {}
    if request.POST.get('action') == 'post':
        for product in json.loads(request.POST.get('products')):
            product_id = int(product['productid'])
            product_qty = int(product['productqty'])
            products[product_id] = {'productid': str(product_id),
                                         'productqty': str(product_qty),
                                         'productTotalPrice': str(Product.objects.get(id=product_id).price * product_qty)}
            basket.update(product=product_id, qty=product_qty)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'products':products, 'qty': basketqty, 'subtotal': f"${baskettotal}"})
        return response  