import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_product_list_require_auth(api_client):
    url=reverse("products-list")
    response=api_client.get(url)

    assert response.status_code == 401


    