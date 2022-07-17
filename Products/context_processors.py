from .models import Category, Brand

def products(request):
    return {'categories': Category.objects.all(), 'brands': Brand.objects.all()}