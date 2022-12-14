from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ecommerce.apps.catalog.urls", namespace="catalog")),
    path("basket/", include("ecommerce.apps.basket.urls", namespace="basket")),
    path(
        "account/", include("ecommerce.apps.account.urls", namespace="account")
    ),
    path(
        "payment/", include("ecommerce.apps.payment.urls", namespace="payment")
    ),
    path("orders/", include("ecommerce.apps.orders.urls", namespace="orders")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
