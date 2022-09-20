from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        current_site = get_current_site(None)
        subject = "Activate your Account"
        message = render_to_string(
            "accounts/account_activation_email.html",
            {
                "user": instance,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
                "token": account_activation_token.make_token(instance),
            },
        )
        instance.email_user(subject=subject, message=message)
        