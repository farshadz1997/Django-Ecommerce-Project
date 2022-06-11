from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.views.generic import ListView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RegistrationForm, UserEditForm, UserLoginForm, PwdResetForm, PwdResetConfirmForm, AddressForm
from .models import UserBase
from .tokens import account_activation_token


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm
    success_url = reverse_lazy('accounts:dashboard')
    redirect_authenticated_user = True

@login_required()
def dashboard(request):
    return render(request, 'accounts/user/dashboard.html')

def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            messages.success(request, 'Your account has been created! Activation email sent to your email.')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        registerForm = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now login.')
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/activation_invalid.html')
    
class PasswordReset(auth_views.PasswordResetView):
    # url name: pwdreset
    template_name = 'accounts/user/default_form.html'
    success_url = reverse_lazy('accounts:pwdreset_done')
    email_template_name = 'accounts/user/password_reset_email.html'
    form_class = PwdResetForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        return super().dispatch(request, *args, **kwargs)
    
class PasswordResetConfirm(SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    # url name: pwdreset_confirm
    template_name = 'accounts/user/default_form.html'
    success_url = reverse_lazy('accounts:login')
    form_class = PwdResetConfirmForm
    success_message = "Your password changed successfully, you may login now."

class ChangePassword(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    # url name: change_password
    template_name = 'accounts/user/default_form.html'
    success_url = reverse_lazy('accounts:dashboard')
    success_message = "Password changed successfully"
    
class ChangeUserDetail(SuccessMessageMixin, LoginRequiredMixin, FormView):
    # url name: edit_details
    template_name = 'accounts/user/default_form.html'
    success_url = reverse_lazy('accounts:dashboard')
    success_message = "Username changed successfully"
    form_class = UserEditForm
    extra_context = {"title": "Change User detail"}
    
    def get_form(self, form_class=form_class):
        return form_class(instance = self.request.user, **self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)

class DeleteUser(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserBase.objects.get(user_name=request.user)
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, 'Your account has been deleted successfully')
        return redirect('accounts:login')

class AddressView(SuccessMessageMixin, LoginRequiredMixin, FormView):
    model = UserBase
    form_class = AddressForm
    success_message = "Address added successfully"
    success_url = reverse_lazy('accounts:dashboard')
    template_name = "accounts/user/address.html"
    extra_context = {"title": "Address"}
    
    def get_form(self, form_class=form_class):
        return form_class(instance = self.request.user, **self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)