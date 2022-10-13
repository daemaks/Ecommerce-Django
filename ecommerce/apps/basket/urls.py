from django.urls import path

from . import views

app_name = "basket"

urlpatterns = [
    path("", views.basket_summary, name="summary_url"),
    path("add/", views.basket_add, name="add_url"),
    path("delete/", views.basket_delete, name="delete_url"),
    path("update/", views.basket_update, name="update_url"),
]
