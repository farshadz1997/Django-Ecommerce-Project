from django.urls import path
from . import views

app_name = 'Products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='Product_list'),
    path('<int:pk>/<str:slug>/', views.ProductDetailView.as_view(), name='Product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='Product_search'),
    path('categories/<str:category>/', views.ProductCategoryView.as_view(), name='Product_category'),
    path('brands/<str:brand>/', views.ProductBrandView.as_view(), name='Product_brand'),
    path('onsale/', views.ProductOnSaleView.as_view(), name='Product_onsale'),
    path('recently-viewed/', views.ProductRecentlyViewdView.as_view(), name='Product_recently_viewed'),
    path('top-sellers/', views.ProductTopSellersView.as_view(), name='top_sellers'),
]