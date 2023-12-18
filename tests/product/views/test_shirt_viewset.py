from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from iati_test.product.enums import SizeType
from iati_test.product.models import Shirt

from tests.product.factories import MaterialFactory, ShirtFactory


class ShirtViewSetTest(APITestCase):
    def setUp(self):
        self.shirts = ShirtFactory.create_batch(5)
        self.deactivated_shirts = ShirtFactory.create_batch(5, is_active=False)

    def test_list_shirts(self):
        url = reverse("product:shirt-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.shirts))

    def test_retrieve_shirt(self):
        url = reverse("product:shirt-detail", args=[self.shirts[0].id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.shirts[0].id)
        self.assertFalse("initial_stock" in response.data)

    def test_create_shirt(self):
        material_1 = MaterialFactory.create(name="cotton")
        material_2 = MaterialFactory.create(name="polyester")

        url = reverse("product:shirt-list")
        shirt_data = {
            "main_color": "white",
            "secondary_color": "green",
            "brand": "nike",
            "picture_url": "https://www.snipes.es/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw4670d82e/2254784_P.jpg?sw=780&sh=780&sm=fit&sfrm=png",
            "price_per_unit": 39.99,
            "initial_stock": 10,
            "current_stock": 10,
            "catalog_inclusion_date": "2021-01-01",
            "size": "M",
            "size_type": SizeType.WOMAN.value,
            "sleeves": False,
            "materials": [
                {
                    "material_name": material_1.name,
                    "percentage": 10,
                },
                {
                    "material_name": material_2.name,
                    "percentage": 90,
                },
            ],
        }
        response = self.client.post(url, shirt_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shirt.objects.count(), 11)

        shirt = Shirt.objects.get(id=response.data["id"])
        self.assertEqual(shirt.main_color, shirt_data["main_color"])
        self.assertEqual(shirt.secondary_color, shirt_data["secondary_color"])
        self.assertEqual(shirt.brand, shirt_data["brand"])
        self.assertEqual(float(shirt.price_per_unit), shirt_data["price_per_unit"])
        self.assertEqual(shirt.initial_stock, shirt_data["initial_stock"])
        self.assertEqual(shirt.materials.count(), 2)
        self.assertEqual(shirt.materials.first(), material_1)
        self.assertEqual(shirt.materials.last(), material_2)

    def test_soft_delete_shirt(self):
        shirt = self.shirts[0]

        url = reverse("product:shirt-detail", args=[shirt.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        shirt.refresh_from_db()

        self.assertFalse(shirt.is_active)
        self.assertIsNotNone(shirt.deactivated_at)

    def test_invalid_update_shirt(self):
        shirt = self.shirts[0]

        url = reverse("product:shirt-detail", args=[shirt.id])
        data = {
            "initial_stock": 150,
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_shirt(self):
        shirt = self.shirts[0]

        url = reverse("product:shirt-detail", args=[shirt.id])
        data = {
            "current_stock": shirt.current_stock + 10,
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shirt.refresh_from_db()
        self.assertEqual(shirt.current_stock, data["current_stock"])
