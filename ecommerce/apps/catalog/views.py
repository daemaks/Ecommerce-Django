from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def categories(request):
    return {"categories": Category.objects.filter(level=0)}


def products_list(request):
    context = Product.objects.prefetch_related("product_image").filter(
        is_active=True
    )
    return render(request, "catalog/products_list.html", {"products": context})


def product_details(request, slug):
    context = get_object_or_404(Product, slug=slug, is_active=True)
    return render(
        request, "catalog/product_details.html", {"product": context}
    )


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    context = Product.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(
            include_self=True
        )
    )
    return render(
        request,
        "catalog/category_list.html",
        {"category": category, "products": context},
    )
