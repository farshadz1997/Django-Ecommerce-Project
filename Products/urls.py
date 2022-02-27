from django.urls import path
from .views import ProductListView, ProductDetailView, ProductSearchView, ProductCategoryView

app_name = 'Products'

urlpatterns = [
    path('', ProductListView.as_view(), name='Product_list'),
    path('<int:pk>/<str:slug>/', ProductDetailView.as_view(), name='Product_detail'),
    path('search/', ProductSearchView.as_view(), name='Product_search'),
    path('category/<str:category>/', ProductCategoryView.as_view(), name='Product_category'),
]