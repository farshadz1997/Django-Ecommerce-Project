from django.shortcuts import redirect
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/', views.account_activate, name='activate'),
    # Password reset
    path('password-reset/', views.PasswordReset.as_view(), name='pwdreset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/user/password_reset_done.html'), name='pwdreset_done'),
    path('password-reset-confirm/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name='pwdreset_confirm'),
    # profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('details/', views.ChangeUserDetail.as_view(), name='edit_details'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('delete-user/', views.DeleteUser.as_view(), name='delete_user'),
]
