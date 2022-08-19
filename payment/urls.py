from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payment, name='pay'),
    path('orderplaced/', views.OrderPlacedView.as_view(), name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),
]
