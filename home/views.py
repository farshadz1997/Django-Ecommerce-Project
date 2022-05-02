from django.shortcuts import render, get_list_or_404, get_object_or_404
from Products.models import Product, Category
from django.views.generic.base import TemplateView


class HomePage(TemplateView):
    template_name = 'home/index.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['Latest_products'] = Product.objects.all().order_by('-pub_date')[:8]
        return context
    