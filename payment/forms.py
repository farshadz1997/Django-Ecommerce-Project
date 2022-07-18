from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML

from accounts.models import Address

class PaymentForm(forms.Form):
    addresses = forms.ModelChoiceField(None)
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["addresses"] = forms.ModelChoiceField(Address.objects.filter(customer=user), label="Address", required=True, blank=False,
                                                          initial=Address.objects.get(customer=user, default=True),
                                                          widget=forms.Select(attrs={"class": "form-control lazyselect form-select"}))
        self.helper = FormHelper()
        self.helper.form_class = "row g-3"
        self.helper.layout = Layout(
            Div('addresses', css_class='form-group col-md-12'),
            HTML('<hr class="col-md-12 my-4">'),
            HTML('<h4 class="col-md-12">Payment</h4>'),
            HTML('<label for="card-element">Credit or debit card</label>'),
            HTML('<div id="card-element" class="form-control form-control-payment"></div>'),
            HTML('<hr class="my-4">'),
            Div(HTML('<button id="submit" type="submit" class="btn-outline-info" data-secret="{{ client_secret }}">Pay</button>'), css_class="form-group"),
            HTML('<br>'),
        )
    