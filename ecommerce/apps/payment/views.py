import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from ecommerce.apps.account.models import Address
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.orders.models import Order, OrderItem
from paypalcheckoutsdk.orders import OrdersGetRequest

from .models import DeliveryOptions
from .paypal import PayPalClient


@login_required
def delivery_choices(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    return render(
        request,
        "payment/delivery_choices.html",
        {"delivery_options": delivery_options},
    )


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("delivery_option"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        update_total_price = basket.update_delivery(
            delivery_type.delivery_price
        )

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        return JsonResponse(
            {
                "total_price": update_total_price,
                "delivery_price": delivery_type.delivery_price,
            }
        )


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please selecet delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by(
        "-default"
    )
    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True
    return render(
        request, "payment/delivery_address.html", {"addresses": addresses}
    )


@login_required
def payment_selection(request):
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "payment/payment_selection.html", {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[
            0
        ].shipping.address.address_line_1,
        address2=response.result.purchase_units[
            0
        ].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[
            0
        ].shipping.address.postal_code,
        country_code=response.result.purchase_units[
            0
        ].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(
            order_id=order_id,
            product=item["product"],
            price=item["price"],
            quantity=item["qty"],
        )

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "payment/payment_successful.html", {})
