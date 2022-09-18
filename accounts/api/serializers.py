from accounts.models import Address
from rest_framework import serializers
from django_countries.serializer_fields import CountryField


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)
    
    class Meta:
        model = Address
        exclude = ("created_at", "updated_at", "customer", "delivery_instructions")