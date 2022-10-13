import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_list_url(client):
    url = reverse("catalog:products_list_url")
    response = client.get(url)
    assert response.status_code == 200
