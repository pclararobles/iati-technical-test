from django.test import TestCase

from iati_test.product.tasks import update_product_stock
from tests.cart.factories import CartProductFactory
from tests.product.factories import CapFactory, ShirtFactory


class UpdateProductStockTest(TestCase):
    def setUp(self):
        # Create instances of Caps and Shirts with initial stock
        self.cap = CapFactory.create(initial_stock=10)
        self.shirt = ShirtFactory.create(initial_stock=20)

        # Create CartProducts reducing the stock
        CartProductFactory.create(cap=self.cap, shirt=None, quantity=4)
        CartProductFactory.create(cap=None, shirt=self.shirt, quantity=5)

    def test_update_product_stock(self):
        update_product_stock()

        self.cap.refresh_from_db()
        self.shirt.refresh_from_db()

        self.assertEqual(self.cap.current_stock, 6)  # 10 initial - 4 used
        self.assertEqual(self.shirt.current_stock, 15)  # 20 initial - 5 used
