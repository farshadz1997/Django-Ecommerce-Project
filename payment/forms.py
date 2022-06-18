from django import forms
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, Button, HTML

from accounts.models import UserBase

class PaymentForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, label='Email', required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'foo@bar.com'}))
    first_name = forms.CharField(label='First Name', max_length=50, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=50, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    address_line_1 = forms.CharField(label='Address Line 1', max_length=50, required=True,
                                     widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    address_line_2 = forms.CharField(label='Address Line 2', max_length=50, required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'Apartmant, Suite, Floor'}))
    country = CountryField(blank_label='(select country)').formfield(label='Country', required=True,
                                                                     widget=forms.Select(attrs={'placeholder': 'Country', 'class': 'form-control lazyselect form-select'}))
    town_city = forms.CharField(label='City', required=True)
    state = forms.CharField(label='State', required=True)
    postcode = forms.CharField(label='Zipcode', required=True)
    phone_number = forms.IntegerField(label='Phone Number', required=True)
    
    class Meta:
        model = UserBase
        fields = ('email', 'first_name', 'last_name', 'address_line_1', 'address_line_2', 'country', 'town_city', 'state', 'postcode', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('first_name', css_class='form-group col-md-5'),
                Div('last_name', css_class='form-group col-md-5'),
                Div('phone_number', css_class='form-group col-md-5'),
                Div('email', css_class='form-group col-md-5'),
                Div('address_line_1', css_class='form-group col-md-10'),
                Div('address_line_2', css_class='form-group col-md-10'),
                Div('country', css_class='form-group col-md-5'),
                Div('state', css_class='form-group col-md-5'),
                Div('town_city', css_class='form-group col-md-5'),
                Div('postcode', css_class='form-group col-md-5'),
                HTML('<hr class="col-md-12 my-4">'),
                HTML('<h4 class="col-md-12">Payment</h4>'),
                HTML('<label for="card-element">Credit or debit card</label>'),
                HTML('<div id="card-element" class="form-control form-control-payment"></div>'),
                HTML('<hr class="my-4">'),
                HTML('<button id="submit" class="btn btn-primary fw-bold" data-secret="{{ client_secret }}">Pay</button>'),
                HTML('<br>'),
                # HTML('<div id="card-element" class="form-control form-control-payment"></div>'),
            css_class='row g-3'
            )
        )
    