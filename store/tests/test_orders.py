import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_create_order(auth_client,product):
    url= reverse("orders-list")
    response=auth_client.post(
        url,
        {
            "product":product.id,
            "quantity":1
        }
    )
    assert response.status_code == 201
    