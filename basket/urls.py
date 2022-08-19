from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.BasketSummaryView.as_view(), name='basket_summary'),
    path('add/', views.basket_add, name = 'basket_add'),
    path('delete/', views.basket_delete, name = 'basket_delete'),
    path('update/', views.basket_update, name = 'basket_update'),
]