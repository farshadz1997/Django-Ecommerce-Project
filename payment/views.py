import json
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from orders.models import Voucher
from .forms import PaymentForm
from basket.basket import Basket
from orders.views import payment_confirmation
from accounts.models import Address, UserBase


class OrderPlacedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        if basket.voucher["discount"] > 0:
            voucher = Voucher.objects.get(voucher_code=basket.voucher["code"])
            if voucher.max_use != None and voucher.max_use > 0:
                voucher.max_use -= 1
                if voucher.max_use == 0:
                    self.clear_expired_discount_from_sessions(voucher.voucher_code)
                voucher.save()
            user = UserBase.objects.get(id=request.user.id)
            user.vouchers.add(voucher)
        basket.clear()
        messages.success(request, 'Your order has been placed')
        return redirect('accounts:orders')
                        
    def clear_expired_discount_from_sessions(self, voucher: str):
        for ses in Session.objects.all():
            session = SessionStore(ses.session_key)
            if 'voucher' in session and session['voucher']['code'] == voucher:
                session['voucher']['code'] = None
                session['voucher']['discount'] = 0
                session.save()


class Error(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        messages.warning(request, 'There was a problem with your payment, please try again')
        return redirect('payment:pay')

@login_required
def payment(request):
    basket = Basket(request)
    if len(basket) == 0:
        messages.warning(request, 'Before proceeding to payment you need to add at least one product to your cart.')
        return redirect('basket:basket_summary')
    if Address.objects.filter(customer=request.user).count() == 0:
        messages.warning(request, 'Please add an address before proceeding.')
        return redirect('accounts:add_address')
    
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    form = PaymentForm(user=request.user)
    STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/checkout.html', {'client_secret': intent.client_secret, 'form': form, 'stripe_public_key': STRIPE_PUBLIC_KEY})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)