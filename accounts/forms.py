from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, PasswordChangeForm)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, MultiField, HTML
from django_countries.fields import CountryField

from .models import UserBase


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Your Email',
            'id': 'login-username'
            }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-group form-row form-row-first'),
            Field('password', css_class='form-group form-row form-row-last'),
            HTML('''<p class="form-row">
                    <input type="submit" value="Login" name="login" class="button">
                    <label class="inline" for="rememberme"><input type="checkbox" value="forever" id="rememberme" name="rememberme"> Remember me </label>
                </p>
                <p class="lost_password">
                    <a href="{%url 'accounts:pwdreset'%}">Lost your password?</a>
                </p>'''),
        )


class RegistrationForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name', min_length=3, max_length=150, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(label='Last Name', min_length=3, max_length=150, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))
    user_name = forms.CharField(label='Username', min_length=4, max_length=50, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Enter a username'}))
    email = forms.EmailField(max_length=100, required=True,
                            error_messages={'required': 'Sorry, you will need an email'},
                            widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'name':'email', 'id':'id_email'}))
    password = forms.CharField(label='Password', required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Repeat password', required=True, 
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'first_name', 'last_name')

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
        self.helper = FormHelper()
        self.helper.form_class = 'account-form p-4 rounded col-xlg-12'
        self.helper.error_text_inline = True
        self.helper.form_show_errors = False
        self.helper.layout = Layout(
            Div('first_name', css_class='form-group col-lg-6'),
            Div('last_name', css_class='form-group col-lg-6'),
            Div('user_name', css_class='form-group col-lg-6 mb-3'),
            Div('email', css_class='form-group col-lg-6 mb-3'),
            Div('password', css_class='form-group col-lg-12 mb-3'),
            Div('password2', css_class='form-group col-lg-12 mb-3'),
            HTML('''<input type="submit" name="register" value="Sign up" class="btn btn-primary btn-block"
                 id="submit-id-register" style="width:96%; margin-left:15px; margin-bottom:25px">''')
        )


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'id': 'form-email'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.error_text_inline = True
        # self.helper.label_class = 'col-sm-4'
        # self.helper.field_class = 'col-sm-5'
        self.helper.layout = Layout(
            Div('email', css_class='form-group mb-3'),
            HTML('<button class="btn-outline-info" type="submit" style="margin-bottom:25px">Reset Password</button>')
            )
    
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
            attrs={'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'placeholder': 'New Password', 'id': 'form-new-pass2'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div('new_password1', css_class='form-group mb-3'),
            Div('new_password2', css_class='form-group mb-3'),
            HTML('<button class="btn-outline-info" type="submit" style="margin-bottom:25px">Change Password</button>')
        )


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, disabled=True, widget=forms.TextInput(
            attrs={'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'id': 'form-username'}))

    first_name = forms.CharField(
        label='First name', min_length=3, max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'Firstname', 'id': 'form-firstname'}))
    
    last_name = forms.CharField(
        label='Last name', min_length=3, max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'Lastname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div('email', css_class='form-group mb-3'),
            Div('user_name', css_class='form-group mb-3'),
            Div('first_name', css_class='form-group mb-3'),
            Div('last_name', css_class='form-group mb-3'),
            Div(
                HTML('<button class="btn-outline-info" type="submit">Update profile</button>'),
                HTML('<a href="{%url "accounts:delete_user"%}" class="btn btn-danger" style="padding: 10px 15px; margin-left: 10px">Delete Account</a>'),
                css_class='form-group'
            )
        )
      
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


class ChangePasswordForm(PasswordChangeForm):
    
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div('old_password', css_class='form-group mb-3'),
            Div('new_password1', css_class='form-group mb-3'),
            Div('new_password2', css_class='form-group mb-3'),
            Div(HTML('<button class="btn-outline-info" type="submit">Change Password</button>'), css_class='form-group')
        )

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
            Field('address_line_1', css_class='form-group col-md-3'),
            Field('address_line_2', css_class='form-group col-md-3'),
            Div(
                Field('country', css_class='form-control'),
                css_class = 'form-group',
            ),
            Row(
                Column('town_city', css_class='form-group col-sm-6 mb-0'),
                Column('state', css_class='form-group col-sm-6 mb-0'),
            ),
            Row(
                Column('phone_number', css_class='form-group col-sm-6 mb-0'),
                Column('postcode', css_class='form-group col-sm-6 mb-0'),
            ),
            Div(HTML('<button class="btn-outline-info" type="submit">Submit</button>'), css_class='form-group'),
        )