from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.products_list, name='products_list_url'),
    path('item/<slug:slug>/', views.product_details, name='product_details_url'),
    path('search/<slug:category_slug>', views.category_list, name='category_list_url'),
]
