from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Address, UserBase


class AddressInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        data = self.cleaned_data
        if len(data) == 0:
            return data
        count_defaults = 0
        for addr in data:
            count_defaults += addr.get("default", 0)
        if count_defaults > 1:
            raise forms.ValidationError("Only one address can be set as default.")
        if count_defaults == 0:
            raise forms.ValidationError("One address required to be set as default.")
        return data

class AddressInlineAdmin(admin.StackedInline):
    model = Address
    formset = AddressInlineFormSet
    extra = 0
    max_num = 4
    fields = (
        'customer',
        ('first_name', 'last_name'),
        'phone',
        ('address_line_1', 'address_line_2'),
        'postcode',
        ('city', 'state', 'country'),
        'delivery_instructions',
        'default',
        )
    classes = ('collapse',)

@admin.register(UserBase)
class UserBaseAdmin(admin.ModelAdmin):
    inlines = [AddressInlineAdmin]
    list_display = ('user_name', 'email', 'is_staff', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('user_name', 'email')
    ordering = ('-created',)

    @admin.display(description=_("created at"))
    def created_at(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M:%S")
    
    @admin.display(description=_("updated at"))
    def updated_at(self, obj):
        return obj.updated.strftime("%Y-%m-%d %H:%M:%S")
    