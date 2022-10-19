from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .api import viewsets

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/accounts/login/"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("activate/<slug:uidb64>/<slug:token>)/", views.ActivateAccount.as_view(), name="activate"),
    # Password reset
    path("password-reset/", views.PasswordReset.as_view(), name="pwdreset"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/user/password_reset_done.html"), name="pwdreset_done"),
    path("password-reset-confirm/<uidb64>/<token>", views.PasswordResetConfirm.as_view(), name="pwdreset_confirm"),
    # Profile
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path("change-password/", views.ChangePassword.as_view(), name="change_password"),
    path("details/", views.ChangeUserDetail.as_view(), name="edit_details"),
    path("delete-user/", views.DeleteUser.as_view(), name="delete_user"),
    path("addresses/", views.UserAddressesView.as_view(), name="addresses"),
    path("addresses/add/", views.AddressCreateView.as_view(), name="add_address"),
    path("addresses/update/<pk>/", views.AddressUpdateView.as_view(), name="update_address"),
    path("addresses/delete/<pk>/", views.AddressDeleteView.as_view(), name="delete_address"),
    path("addresses/default/<pk>/", views.AddressSetDefault.as_view(), name="set_default_address"),
    # Wishlist
    path("wishlist/", views.WishlistView.as_view(), name="wishlist"),
    path("wishlist/add-remove/<id>/", views.AddOrRemoveFromWishlistView.as_view(), name="add-remove-wishlist"),
    # Orders
    path("orders", views.OrdersView.as_view(), name="orders"),
    # API
    path("api/register/", viewsets.RegisterAPI.as_view(), name="api_register"),
    path("api/authenticate/", viewsets.AuthenticateUserAPI.as_view(), name="api_authenticate"),
    path("api/logout/", viewsets.LogoutAPI.as_view(), name="api_logout"),
    path("api/addresses/", viewsets.AddressesAPI.as_view(), name="api_addresses"),
    path("api/address/create/", viewsets.CreateAddressAPI.as_view(), name="api_create_address"),
    path("api/address/<pk>/", viewsets.AddressAPI.as_view(), name="api_modify_address"),
    path("api/change-password/", viewsets.ChangePasswordAPI.as_view(), name="api_change_password"),
    path("api/update-user/", viewsets.UpdateUserAPI.as_view(), name="api_update_user"),
]
