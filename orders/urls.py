from django.urls import path

from . import views
from .api import viewsets as api_viewsets

app_name = 'orders'

urlpatterns = [
    path('add/', views.add, name='add'),
    #### API ####
    path('api/add/', api_viewsets.CreateOrderAPI.as_view(), name='api_add'),
]
