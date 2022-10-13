from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path(
        "deliverychoices/",
        views.delivery_choices,
        name="delivery_choices_url",
    ),
    path(
        "basket_update_delivery/",
        views.basket_update_delivery,
        name="basket_update_delivery_url",
    ),
    path(
        "delivery_address/",
        views.delivery_address,
        name="delivery_address_url",
    ),
    path(
        "payment_selection/",
        views.payment_selection,
        name="selection_url",
    ),
    path(
        "payment_complete/",
        views.payment_complete,
        name="complete_url",
    ),
    path(
        "payment_successful/",
        views.payment_successful,
        name="successful_url",
    ),
]
