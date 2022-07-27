from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('categories/<str:category>/', views.ProductCategoryView.as_view(), name='product_category'),
    path('brands/<str:brand>/', views.ProductBrandView.as_view(), name='product_brand'),
    path('onsale/', views.ProductOnSaleView.as_view(), name='product_onsale'),
    path('recently-viewed/', views.ProductRecentlyViewdView.as_view(), name='product_recently_viewed'),
    path('top-sellers/', views.ProductTopSellersView.as_view(), name='top_sellers'),
]