import uuid
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email address"), unique=True)
    user_name = models.CharField(_("User name"), max_length=150, unique=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    vouchers = models.ManyToManyField("orders.Voucher", related_name="users", blank=True)
    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.user_name

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "Ecommerce-site@store.com",
            [self.email],
            fail_silently=False,
        )
        
    def link_to_user(self):
        """link to user details in the admin site"""
        return format_html(f'<a href="{reverse("admin:accounts_userbase_change", args=(self.id,))}">{self.user_name}</a>')


class Address(models.Model):
    """
    Address
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(UserBase, verbose_name=_("Customer"), related_name="addresses", on_delete=models.CASCADE)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    phone = models.CharField(_("Phone Number"), max_length=20)
    postcode = models.CharField(_("Postcode"), max_length=25)
    address_line_1 = models.CharField(_("Address Line 1"), max_length=75)
    address_line_2 = models.CharField(_("Address Line 2"), max_length=75, blank=True, null=True)
    country = CountryField()
    state = models.CharField(_("State/Province"), max_length=50, blank=False)
    city = models.CharField(_("Town/City"), max_length=50, blank=False)
    delivery_instructions = models.TextField(_("Delivery Instructions"), max_length=500, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.postcode}"
    
    def delete(self, *args, **kwargs):
        super(Address, self).delete(*args, **kwargs)
        if self.default and Address.objects.filter(customer=self.customer).exclude(id=self.id).count() >= 1:
            obj = Address.objects.filter(customer=self.customer).exclude(id=self.id).first()
            obj.default = True
            obj.save()