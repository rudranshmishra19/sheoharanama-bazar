import pytest
from django.urls import reverse
from store.models import CartItem

@pytest.mark.django_db
def test_add_item_to_cart(auth_client, product):
    """
    Authenticated user can add a product to cart

    """
    url = reverse("cartitems-list")

    response =auth_client.post(
        url,
        {
            "product":product.id,
            "quantity":1
        }
    )
    assert response.status_code == 201
    assert CartItem.objects.count() ==1


