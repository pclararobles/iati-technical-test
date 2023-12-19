from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from iati_test.cart.models import Cart, CartProduct
from tests.cart.factories import CartFactory, CartProductFactory
from tests.product.factories import CapFactory, ShirtFactory


class CartViewTestCase(APITestCase):
    def setUp(self):
        self.shirts = ShirtFactory.create_batch(5)
        self.caps = CapFactory.create_batch(5)
        self.url = reverse("cart:cart-view")

    def _success_assertions(self, response, cap, shirt):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.first().products.count(), 2)

        cap.refresh_from_db()
        shirt.refresh_from_db()
        self.assertEqual(cap.current_stock, cap.initial_stock - 2)
        self.assertEqual(shirt.current_stock, shirt.initial_stock - 1)

        CartProduct.objects.filter(cap=cap).first().quantity == 2
        CartProduct.objects.filter(shirt=shirt).first().quantity == 1

    def test_post_success_cart_unexistent(self):
        cap = self.caps[0]
        shirt = self.shirts[0]
        data = {
            "products": [
                {"cap_id": cap.id, "shirt_id": None, "quantity": 2},
                {"cap_id": None, "shirt_id": shirt.id, "quantity": 1},
            ]
        }

        self.assertEqual(Cart.objects.count(), 0)

        response = self.client.post(self.url, data, format="json")

        self._success_assertions(response, cap, shirt)

    def test_post_cart_existent(self):
        cart = CartFactory()
        cap = self.caps[0]
        shirt = self.shirts[0]
        data = {
            "products": [
                {"cap_id": cap.id, "shirt_id": None, "quantity": 2},
                {"cap_id": None, "shirt_id": shirt.id, "quantity": 1},
            ]
        }

        self.assertEqual(Cart.objects.count(), 1)

        response = self.client.post(self.url, data, format="json")

        self._success_assertions(response, cap, shirt)

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.first().id, cart.id)

        data = {
            "products": [
                {"cap_id": cap.id, "shirt_id": None, "quantity": -1},
                {"cap_id": None, "shirt_id": shirt.id, "quantity": 3},
            ]
        }

        response = self.client.post(self.url, data, format="json")

        cap.refresh_from_db()
        shirt.refresh_from_db()
        self.assertEqual(cap.current_stock, cap.initial_stock - 1)
        self.assertEqual(shirt.current_stock, shirt.initial_stock - 4)

        CartProduct.objects.filter(cap=cap).first().quantity == 1
        CartProduct.objects.filter(shirt=shirt).first().quantity == 4

        data = {
            "products": [
                {"cap_id": cap.id, "shirt_id": None, "quantity": -5},
            ]
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        cap.refresh_from_db()
        data = {
            "products": [
                {"cap_id": cap.id, "shirt_id": None, "quantity": cap.current_stock + 1},
            ]
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_success(self):
        cart = CartFactory()
        cap = self.caps[0]
        shirt = self.shirts[0]
        cart_product_cap = CartProductFactory(cart=cart, cap=cap, quantity=2, shirt=None)
        cart_product_shirt = CartProductFactory(cart=cart, shirt=shirt, quantity=1, cap=None)

        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], cart.id)
        self.assertEqual(len(response.data["products"]), 2)
        self.assertEqual(response.data["products"][0]["cap_id"], cap.id)
        self.assertEqual(response.data["products"][0]["quantity"], cart_product_cap.quantity)
        self.assertEqual(response.data["products"][0]["shirt_id"], None)
        self.assertEqual(response.data["products"][1]["cap_id"], None)
        self.assertEqual(response.data["products"][1]["quantity"], cart_product_shirt.quantity)
        self.assertEqual(response.data["products"][1]["shirt_id"], shirt.id)
