from django.contrib import admin

from .models import Address, UserBase

admin.site.register(UserBase)
admin.site.register(Address)
