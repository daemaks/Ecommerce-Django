from django.urls import reverse


def test_category_str(product_category):
    assert product_category.__str__() == "category_test"


def test_category_url(client, product_category):
    category = product_category
    url = reverse("catalog:category_list_url", args=[category.slug])
    response = client.get(url)
    assert response.status_code == 200


def test_product_type_str(product_type):
    assert product_type.__str__() == "product_type_test"


def test_product_specification_str(product_specification):
    assert product_specification.__str__() == "product_specification_test"


def test_product_str(product):
    assert product.__str__() == "product_test"


def test_product_url(client, product):
    product = product
    url = reverse("catalog:product_details_url", args=[product.slug])
    response = client.get(url)
    assert response.status_code == 200


def test_product_specification_value_str(product_specification_value):
    assert product_specification_value.__str__() == "value_test"
