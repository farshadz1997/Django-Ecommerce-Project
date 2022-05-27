from django.shortcuts import redirect
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/', views.account_activate, name='activate'),
]
