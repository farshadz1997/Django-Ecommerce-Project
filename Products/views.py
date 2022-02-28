from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'Products/Product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'Products/Product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['recent_products'] = Product.objects.all().order_by('-pub_date')[:4]
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(pk=self.object.pk)[:4]
        return context
    
class ProductSearchView(ListView):
    template_name = 'Products/Product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context
    
    def get_queryset(self):
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            return Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
class ProductCategoryView(ListView):
    template_name = 'Products/Product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category'])