from django.urls import path

from . import views
from .api import viewsets as api_viewsets

app_name = 'payment'

urlpatterns = [
    path('', views.payment, name='pay'),
    path('orderplaced/', views.OrderPlacedView.as_view(), name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),
    ######## API ########
    path("api/pay/", api_viewsets.PaymentAPI.as_view(), name="payment_api"),
]
