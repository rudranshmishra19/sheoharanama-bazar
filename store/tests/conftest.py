import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Customer, Product,Cart,Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user=User.objects.create_user(
        username="testuser",
        password="testpass123"
    )
    Customer.objects.create(user=user)
    Cart.objects.create(customer=user.customer)
    return user

@pytest.fixture
def auth_client(api_client,user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Test Category"
    )
@pytest.fixture
def product(db,category):
    return Product.objects.create(
        name="Test Product",
        price=100,
        stock=10,
        available=True,
        category=category

    )

