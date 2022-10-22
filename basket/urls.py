from django.urls import path
from . import views
from .api import viewsets

app_name = 'basket'

urlpatterns = [
    path('', views.BasketSummaryView.as_view(), name='basket_summary'),
    path('add/', views.basket_add, name = 'basket_add'),
    path('delete/', views.basket_delete, name = 'basket_delete'),
    path('update/', views.basket_update, name = 'basket_update'),
    # API
    path('api/overview/', viewsets.BasketOverviewAPI.as_view(), name='basket_overview_api'),
    path('api/detail/', viewsets.BasketDetailAPI.as_view(), name='basket_detail_api'),
    path('api/voucher/', viewsets.VoucherAPI.as_view(), name='voucher_api'),
]