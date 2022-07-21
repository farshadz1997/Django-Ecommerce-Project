from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0
    

@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    fields = ('user', 
              'address', 
              ('first_name', 'last_name'), 
              'phone', 
              ('address_line_1', 'address_line_2'), 
              'postcode', 
              ('city', 'state', 'country'), 
              'delivery_instructions',
              'total_paid',
              'order_key',
              'billing_status')
    list_display = ('id', 'link_to_user', 'address', 'total_paid', 'created_at', 'billing_status')
    list_filter = ('billing_status',)
    readonly_fields = ('order_key',)
    search_fields = ('id',)
    inlines = [OrderItemInLine]
    
    @admin.display(description=_("created at"))
    def created_at(self, obj):
        return obj.created.strftime('%Y-%m-%d %H:%M:%S')
    
    @admin.display(description=_("user"))
    def link_to_user(self, obj):
        return obj.user.link_to_user()