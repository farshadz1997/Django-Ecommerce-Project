from .models import Category, Brand
from django.db.models import Count

def products(request):
    return {
        'categories': Category.objects.all().annotate(count=Count('products')),
        'brands': Brand.objects.all().annotate(count=Count('products'))
        }