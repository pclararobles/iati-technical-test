from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from iati_test.product.models import Cap

from tests.product.factories import CapFactory


class CapViewSetTest(APITestCase):
    def setUp(self):
        self.caps = CapFactory.create_batch(5)
        self.deactivated_caps = CapFactory.create_batch(5, is_active=False)

    def test_list_caps(self):
        url = reverse("product:cap-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.caps))

    def test_retrieve_cap(self):
        url = reverse("product:cap-detail", args=[self.caps[0].id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.caps[0].id)
        self.assertFalse("initial_stock" in response.data)

    def test_create_cap(self):
        url = reverse("product:cap-list")
        cap_data = {
            "main_color": "grey",
            "secondary_color": "black",
            "brand": "New Era",
            "picture_url": "https://hatstore.imgix.net/197706759995_1.jpg?auto=compress%2Cformat&w=544&h=435&fit=crop&q=50",
            "catalog_inclusion_date": "2021-01-01",
            "initial_stock": 10,
            "current_stock": 10,
            "price_per_unit": 34.99,
            "logo_color": "black",
        }
        response = self.client.post(url, cap_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cap.objects.count(), 11)

        cap = Cap.objects.get(id=response.data["id"])
        self.assertEqual(cap.main_color, cap_data["main_color"])
        self.assertEqual(cap.secondary_color, cap_data["secondary_color"])
        self.assertEqual(cap.brand, cap_data["brand"])
        self.assertEqual(float(cap.price_per_unit), cap_data["price_per_unit"])
        self.assertEqual(cap.initial_stock, cap_data["initial_stock"])

    def test_soft_delete_cap(self):
        cap = self.caps[0]

        url = reverse("product:cap-detail", args=[cap.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cap.refresh_from_db()

        self.assertFalse(cap.is_active)
        self.assertIsNotNone(cap.deactivated_at)

    def test_invalid_update_cap(self):
        cap = self.caps[0]

        url = reverse("product:cap-detail", args=[cap.id])
        data = {
            "initial_stock": 150,
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_cap(self):
        cap = self.caps[0]

        url = reverse("product:cap-detail", args=[cap.id])
        data = {
            "current_stock": cap.current_stock + 10,
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cap.refresh_from_db()
        self.assertEqual(cap.current_stock, data["current_stock"])
