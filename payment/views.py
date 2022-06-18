import json
from django.http import HttpResponseRedirect
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decouple import config

from .forms import PaymentForm
from basket.basket import Basket
from orders.views import payment_confirmation

@login_required
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    messages.success(request, 'Your order has been placed')
    return redirect('accounts:dashboard')


class Error(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        messages.error(request, 'Your payment was not successful')
        return HttpResponseRedirect(reverse('accounts:dashboard'))


@login_required
def BasketView(request):

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    form = PaymentForm(instance=request.user)
    stripe.api_key = config('STRIPE_SECRET_KEY')
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/checkout.html', {'client_secret': intent.client_secret, 'form': form})


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

