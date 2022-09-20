from accounts.models import UserBase, Address
from rest_framework import serializers
from django_countries.serializer_fields import CountryField


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)
    
    class Meta:
        model = Address
        exclude = ("created_at", "updated_at", "customer", "delivery_instructions")
        
        
class RegisterAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    first_name = serializers.CharField(min_length=3, max_length=150, required=True)
    last_name = serializers.CharField(min_length=3, max_length=150, required=True)
    user_name = serializers.CharField(min_length=3, max_length=50, required=True)
    password= serializers.CharField(required=True)
    password2= serializers.CharField(required=True)
    
    def validate_password2(self, value):
        if value != self.initial_data["password"]:
            raise serializers.ValidationError("Passwords do not match")
        return value
    
    def validate_email(self, value):
        if UserBase.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_user_name(self, value):
        if UserBase.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def create(self, validated_data):
        del validated_data["password2"]
        return UserBase.objects.create(is_active=False, **validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    
    def validate_new_password2(self, value):
        if value != self.initial_data["new_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return value
    

class UpdateAccountSerializer(serializers.ModelSerializer):
    def validate_user_name(self, value):
        characters = (" ","/","'",".","@","#","$","%","^","&","*","+","=","`",
                      "~","!","?",":",";","<",">","{","}","|",'"',",","'","-",)
        if any(char in value for char in characters):
            raise serializers.ValidationError("Username can not contain white space and special characters.")
        if UserBase.objects.filter(user_name=value).exclude(id=self.instance.pk).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    class Meta:
        model = UserBase
        fields = ("user_name", "first_name", "last_name")