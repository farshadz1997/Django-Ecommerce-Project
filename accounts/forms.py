from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, Button, HTML
from django_countries.fields import CountryField

from .models import UserBase


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'id': 'login-username'
            }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, disabled=True, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username'}))

    first_name = forms.CharField(
        label='First name', min_length=3, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
      
    def clean_user_name(self): 
        user_name = self.cleaned_data['user_name'].lower()
        characters = (' ', '/', '\'', '.', '@', '#', '$', '%', '^', '&', '*', '+', '=','`',
                      '~', '!', '?', ':', ';', '<', '>', '{', '}', '|', '"', ',', "'", '-')
        if any(char in user_name for char in characters):
            raise forms.ValidationError(
                "Username can not contain white space and special characters.")
        if UserBase.objects.filter(user_name=user_name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Please use another Username, that is already taken")
        return user_name
    

class AddressForm(forms.ModelForm):
    address_line_1 = forms.CharField(
        label='Address',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_line_2 = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    country = CountryField(blank_label='(select country)').formfield(label='Country', required=True)
    town_city = forms.CharField(label='City', required=True)
    state = forms.CharField(label='State', required=True)
    postcode = forms.CharField(label='Zipcode', required=True)
    phone_number = forms.IntegerField(label='Phone Number', required=True)

    class Meta:
        model = UserBase
        fields = ('address_line_1', 'address_line_2', 'country', 'town_city', 'state', 'postcode', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('address_line_1', css_class='form-group col-md-4'),
                Field('address_line_2', css_class='form-group col-md-4'),
                Div(
                    Field('country', css_class='form-control'),
                    css_class = 'form-group',
                ),
                Row(
                    Column('town_city', css_class='form-group col-md-4 mb-0'),
                    Column('state', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('phone_number', css_class='form-group col-md-4 mb-0'),
                    Column('postcode', css_class='form-group col-sm-4 mb-0'),
                ),
                Submit('submit', 'Submit', css_class='btn-outline-info'),
                HTML('<br>'),
                css_class='col-12 col-lg-6 mx-auto'
            ),
        )