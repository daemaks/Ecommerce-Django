from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ecommerce.apps.catalog.models import Product
from ecommerce.apps.orders.models import Order
from ecommerce.apps.orders.views import user_orders

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, UserBase
from .token import account_activation_token


@login_required
def account_dashboard(request):
    orders = user_orders(request)
    return render(
        request, "account/dashboard/dashboard.html", {"orders": orders}
    )


@login_required
def account_edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(
        request,
        "account/dashboard/account_edit.html",
        {"user_form": user_form},
    )


@login_required
def account_wishlist(request):
    wishlist = Product.objects.filter(user_wishlist=request.user)
    return render(
        request,
        "account/dashboard/account_wishlist.html",
        {"wishlist": wishlist},
    )


@login_required
def account_add_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(
            request, f"{product.title} has been removed from your Wishlist"
        )
    else:
        messages.success(request, f"Added {product.title} to your Wishlist")
        product.user_wishlist.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def account_delete(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation_url")


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard_url")

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data["email"]
            user.set_password(register_form.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(
                request,
                "account/registration/registration_email_confirm.html",
                {"form": register_form},
            )
        else:
            return HttpResponse("Error handler content", status=400)
    else:
        register_form = RegistrationForm()
    return render(
        request, "account/registration/register.html", {"form": register_form}
    )


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard_url")
    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required
def account_addresses(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(
        request,
        "account/dashboard/account_addresses.html",
        {"addresses": addresses},
    )


@login_required
def account_add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses_url"))
        else:
            return HttpResponse("Error handler content", status_code=400)
    else:
        address_form = UserAddressForm()

    return render(
        request,
        "account/dashboard/account_add_address.html",
        {"form": address_form},
    )


@login_required
def account_edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses_url"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(
        request,
        "account/dashboard/account_edit_address.html",
        {"form": address_form},
    )


@login_required
def account_delete_address(request, id):
    Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses_url")


@login_required
def account_set_default_address(request, id):
    Address.objects.filter(customer=request.user, default=True).update(
        default=False
    )
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("payment:delivery_address_url")

    return redirect("account:addresses_url")


@login_required
def account_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(
        request, "account/dashboard/account_orders.html", {"orders": orders}
    )
