from django.urls import path
from . import views
from .api import viewsets

app_name = 'products'

product_list = viewsets.ProductAPI.as_view({'get': 'list'})
product_detail = viewsets.ProductAPI.as_view({'get': 'retrieve'})

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('categories/<str:category>/', views.ProductCategoryView.as_view(), name='product_category'),
    path('brands/<str:brand>/', views.ProductBrandView.as_view(), name='product_brand'),
    path('onsale/', views.ProductOnSaleView.as_view(), name='product_onsale'),
    path('recently-viewed/', views.ProductRecentlyViewdView.as_view(), name='product_recently_viewed'),
    path('top-sellers/', views.ProductTopSellersView.as_view(), name='top_sellers'),
    # API
    path('api/all/', product_list, name='api_product_list'),
    path('api/details/<int:pk>/', product_detail, name='api_product_detail'),
    path('api/create/', viewsets.ProductListCreateAPI.as_view(), name='api_product_create'),
    path('api/categories/<str:category>/', viewsets.CategoryAPI.as_view(), name='api_category_list'),
    path('api/brands/<str:brand>/', viewsets.BrandAPI.as_view(), name='api_brand_list'),
    path('api/on-sale/', viewsets.OnSaleAPI.as_view(), name='api_on_sale'),
    path('api/top-sellers/', viewsets.TopSellersAPI.as_view(), name='api_top_sellers'),
    path('api/search/', viewsets.SearchAPI.as_view(), name='api_search'),
]
