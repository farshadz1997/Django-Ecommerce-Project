from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, DeleteView, UpdateView, View, TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.conf import settings
from django.db.models import Sum
from Products.models import Product
from orders.models import Order

from .forms import (
    AddressForm,
    ChangePasswordForm,
    PwdResetConfirmForm,
    PwdResetForm,
    RegistrationForm,
    UserEditForm,
    UserLoginForm,
)
from .models import Address, UserBase
from .tokens import account_activation_token


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm
    success_url = reverse_lazy("accounts:dashboard")
    redirect_authenticated_user = True


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user/dashboard.html"


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "accounts/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            messages.success(request, "Your account has been created! Activation email sent to your email.")
            return redirect("accounts:login")
    else:
        registerForm = RegistrationForm()
    return render(request, "accounts/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now login.")
        return redirect("accounts:dashboard")
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("accounts:login")


class PasswordReset(auth_views.PasswordResetView):
    # url name: pwdreset
    template_name = "accounts/user/default_form.html"
    success_url = reverse_lazy("accounts:pwdreset_done")
    email_template_name = "accounts/user/password_reset_email.html"
    form_class = PwdResetForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return super().dispatch(request, *args, **kwargs)


class PasswordResetConfirm(SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    # url name: pwdreset_confirm
    template_name = "accounts/user/default_form.html"
    success_url = reverse_lazy("accounts:login")
    form_class = PwdResetConfirmForm
    success_message = "Your password changed successfully, you may login now."


class ChangePassword(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    # url name: change_password
    template_name = "accounts/user/default_form.html"
    success_url = reverse_lazy("accounts:dashboard")
    success_message = "Password changed successfully"
    form_class = ChangePasswordForm


class ChangeUserDetail(LoginRequiredMixin, SuccessMessageMixin, FormView):
    # url name: edit_details
    template_name = "accounts/user/default_form.html"
    success_url = reverse_lazy("accounts:dashboard")
    success_message = "Username changed successfully"
    form_class = UserEditForm
    extra_context = {"title": "Change User detail"}

    def get_form(self, form_class=form_class):
        return form_class(instance=self.request.user, **self.get_form_kwargs())

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
        messages.success(request, "Your account has been deleted successfully")
        return redirect("accounts:login", permanent=True)


class UserAddressesView(LoginRequiredMixin, ListView):
    template_name = "accounts/user/addresses.html"
    context_object_name = "addresses"

    def get_queryset(self, **kwargs):
        return Address.objects.filter(customer=self.request.user)

    
class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Address
    form_class = AddressForm
    success_message = "Address added successfully"
    success_url = reverse_lazy("accounts:addresses")
    template_name = "accounts/user/default_form.html"
    extra_context = {"title": "Add Address"}
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse(settings.LOGIN_URL)}?next={request.path}")
        if Address.objects.filter(customer=self.request.user).count() < 4:
            return super().dispatch(request, *args, **kwargs)
        messages.warning(request, "You have reached to maximum number of addresses")
        return redirect("accounts:addresses")
            
    def form_valid(self, form):
        if Address.objects.filter(customer=self.request.user, default=True).count() == 0:
            form.instance.default = True
        form.instance.customer = self.request.user
        return super().form_valid(form)
    
    
class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Address
    form_class = AddressForm
    success_message = "Address updated successfully"
    success_url = reverse_lazy("accounts:addresses")
    template_name = "accounts/user/default_form.html"
    extra_context = {"title": "Update address"}

    def test_func(self):
        address = self.get_object()
        if self.request.user == address.customer:
            return True
        return False
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)


class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Address
    success_url = reverse_lazy("accounts:addresses")
    success_message = "Address deleted successfully"

    def test_func(self):
        address = self.get_object()
        if address.customer == self.request.user:
            return True
        return False  
    
    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.customer == self.request.user:
            raise Http404
        return obj


class AddressSetDefault(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        address = Address.objects.get(pk=self.kwargs.get("pk"))
        if address.customer == self.request.user:
            return True
        return False
    
    def get(self, request, *args, **kwargs):
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(pk=self.kwargs.get("pk"), customer=request.user).update(default=True)
        messages.success(request, "Address has been set to default.")
        return redirect("accounts:addresses")
    

class WishlistView(LoginRequiredMixin, ListView):
    context_object_name = "products"
    template_name = "Products/Product_list.html"
    paginate_by = 12
    
    def get_queryset(self):
        return Product.products.filter(user_wishlist=self.request.user)

    
class AddOrRemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs.get("id"))
        if product.user_wishlist.filter(id=request.user.id).exists():
            product.user_wishlist.remove(request.user)
            messages.success(request, "Product removed from wishlist")
        else:
            product.user_wishlist.add(request.user)
            messages.success(request, f"{product.title} added to your WishList")
        return redirect(request.META["HTTP_REFERER"])
    

class OrdersView(LoginRequiredMixin, ListView):
    template_name = "accounts/user/orders.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        return Order.orders.filter(user=self.request.user, billing_status=True).annotate(items_qty=Sum('items__quantity')).order_by('-created')