import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from tests.product.factories import CapFactory, ShirtFactory


@pytest.mark.django_db
def test_products_api_view():
    client = APIClient()
    # Create test data using factories
    shirts = ShirtFactory.create_batch(5)
    caps = CapFactory.create_batch(5)

    url = reverse("product:products-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data["shirts"]) == len(shirts)
    assert len(response.data["caps"]) == len(caps)

    # Assert that shirts are ordered by catalog_inclusion_date
    shirts_dates = [shirt["catalog_inclusion_date"] for shirt in response.data["shirts"]]
    assert shirts_dates == sorted(shirts_dates)

    # Assert that caps are ordered by catalog_inclusion_date
    caps_dates = [cap["catalog_inclusion_date"] for cap in response.data["caps"]]
    assert caps_dates == sorted(caps_dates)
