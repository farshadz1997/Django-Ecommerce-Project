from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.conf import settings
import stripe
from basket.basket import Basket


class PaymentAPI(APIView):
    """Front gets the payment details from this view and do card validation on frontend"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        total = str(basket.get_total_price())
        total = total.replace('.', '')
        total = int(total)

        STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='usd',
            metadata={'userid': request.user.id}
        )
        return Response({"client_secret": intent.client_secret, "stripe_public_key": STRIPE_PUBLIC_KEY}, status=status.HTTP_200_OK)