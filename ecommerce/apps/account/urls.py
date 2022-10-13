from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = "account"

urlpatterns = [
    # Registration
    path("register/", views.account_register, name="register_url"),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        views.account_activate,
        name="activate_url",
    ),
    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html",
            form_class=UserLoginForm,
        ),
        name="login_url",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/account/login/"),
        name="logout_url",
    ),
    # Dashboard
    path("dashboard/", views.account_dashboard, name="dashboard_url"),
    path("profile/edit/", views.account_edit, name="edit_url"),
    path("profile/delete/", views.account_delete, name="delete_url"),
    path(
        "profile/delete_confirm/",
        TemplateView.as_view(
            template_name="account/dashboard/delete_confirm.html"
        ),
        name="delete_confirmation_url",
    ),
    path(
        "wishlist/add_to_wishlist/<int:id>",
        views.account_add_wishlist,
        name="add_wishlist_url",
    ),
    path("wishlist/", views.account_wishlist, name="wishlist_url"),
    path("orders/", views.account_orders, name="orders_url"),
    # Dashboard/Addresses
    path("addresses/", views.account_addresses, name="addresses_url"),
    path(
        "add_address/",
        views.account_add_address,
        name="add_address_url",
    ),
    path(
        "addresses/edit/<slug:id>/",
        views.account_edit_address,
        name="edit_address_url",
    ),
    path(
        "addresses/delete/<slug:id>/",
        views.account_delete_address,
        name="delete_address_url",
    ),
    path(
        "addresses/set_default/<slug:id>/",
        views.account_set_default_address,
        name="set_default_address_url",
    ),
    # Password Reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="password_reset_url",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password_reset_confirm.html",
            success_url="/account/password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm_url",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(
            template_name="account/password/reset_status.html"
        ),
        name="password_reset_done_url",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(
            template_name="account/password/reset_status.html"
        ),
        name="password_reset_complete_url",
    ),
]
