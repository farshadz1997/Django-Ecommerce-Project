import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from orders.forms import VoucherForm
from orders.models import Voucher
from django.contrib import messages
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView

from .basket import Basket


class BasketSummaryView(FormView):
    template_name = "basket/basket_summary.html"
    form_class = VoucherForm
    success_url = reverse_lazy("basket:basket_summary")

    def get_form(self, form_class=form_class):
        return form_class(self.request.user.id, **self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "In order to use promo codes you need to be logged in.")
            return redirect(f"{reverse(settings.LOGIN_URL)}?next={request.path}")
        form = self.get_form()
        self.basket = Basket(request)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(BasketSummaryView, self).get_context_data(**kwargs)
        context["basket"] = self.basket if self.request.method == "POST" else Basket(self.request)
        context["recent_products"] = Product.products.all()[:4]
        context["offers"] = Product.products.order_by("?").exclude(id__in=context["basket"].basket.keys())[:2]
        return context
    
    def form_valid(self, form):
        voucher = Voucher.objects.get(voucher_code=form.cleaned_data['voucher_code'])
        self.basket.set_discount(voucher.voucher_code, voucher.discount)
        messages.success(self.request, f'%{voucher.discount} discount applied successfully.')
        return super(BasketSummaryView, self).form_valid(form)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        if product.quantity < product_qty:
            response = JsonResponse({"error": f"Not enough {product.title} available in stock."})
            return response
        basket.add(product=product, qty=product_qty)

        baskettottal = basket.get_total_price_without_discount()
        basketqty = basket.__len__()
        response = JsonResponse({"qty": basketqty, "subtotal": f"${baskettottal}"})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        priceWithDiscount = basket.get_total_price()
        priceWithoutDiscount = basket.get_total_price_without_discount()
        response = JsonResponse({"qty": basketqty, "subtotal": f"${priceWithDiscount}", "cart_subtotal": f"${priceWithoutDiscount}"})
        return response


def basket_update(request):
    basket = Basket(request)
    products = {}
    if request.POST.get("action") == "post":
        for product in json.loads(request.POST.get("products")):
            product_id = int(product["productid"])
            product_qty = int(product["productqty"])
            p = get_object_or_404(Product, id=product_id)
            product_final_price = str(p.final_price * product_qty)
            products[product_id] = {
                "productid": str(product_id),
                "productqty": str(product_qty),
                "productTotalPrice": product_final_price,
            }
            basket.update(product=product_id, qty=product_qty)
        basketqty = basket.__len__()
        priceWithDiscount = basket.get_total_price()
        priceWithoutDiscount = basket.get_total_price_without_discount()
        response = JsonResponse({"products": products, "qty": basketqty, "subtotal": f"${priceWithDiscount}", "cart_subtotal": f"${priceWithoutDiscount}" })
        return response
