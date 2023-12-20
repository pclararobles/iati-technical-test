from django.urls import reverse
from rest_framework.test import APITestCase

from iati_test.cart.models import Cart
from tests.cart.factories import CartFactory


class PurchaseViewTestCase(APITestCase):
    def setUp(self):
        self.purchase_url = reverse("cart:purchase")

    def test_purchase_with_active_cart(self):
        cart = CartFactory()

        data = {
            "first_name": "John",
            "last_name": "Doe",
            "postal_address": "123 Main St",
            "email": "john@example.com",
            "phone": "1234567890",
        }

        # Send POST request
        response = self.client.post(self.purchase_url, data, format="json")

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Purchase successful and email sent")

        cart.refresh_from_db()
        self.assertTrue(cart.is_purchased)
        self.assertFalse(Cart.objects.filter(is_purchased=False).exists())

    def test_purchase_without_active_cart(self):
        # Ensure no active cart exists
        Cart.objects.all().delete()

        # Prepare request data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "postal_address": "123 Main St",
            "email": "john@example.com",
            "phone": "1234567890",
        }

        # Send POST request
        response = self.client.post(self.purchase_url, data, format="json")

        # Assert the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["message"], "No active cart found")
