from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from ecommerce.apps.catalog.models import Product

from .basket import Basket


def basket_summary(request):
    context = Basket(request)
    return render(request, "basket/basket_summary.html", {"basket": context})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({"qty": basket_qty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)
        basket_qty = basket.__len__()
        basket_tprice = basket.get_total_price()
        response = JsonResponse(
            {"qty": basket_qty, "total_price": basket_tprice}
        )
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        basket.update(product=product_id, qty=product_qty)
        basket_qty = basket.__len__()
        basket_tprice = basket.get_total_price()
        response = JsonResponse(
            {"qty": basket_qty, "total_price": basket_tprice}
        )
        return response
