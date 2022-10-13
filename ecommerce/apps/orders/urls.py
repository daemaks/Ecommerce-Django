from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("add/", views.orders_add, name="orders_add_url"),
]
