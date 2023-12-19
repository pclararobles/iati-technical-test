import factory
from factory.django import DjangoModelFactory
from datetime import date
from iati_test.cart.models import Cart, CartProduct
from tests.product.factories import CapFactory, ShirtFactory


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    date = factory.LazyFunction(date.today)
    is_purchased = False


class CartProductFactory(DjangoModelFactory):
    class Meta:
        model = CartProduct

    cart = factory.SubFactory(CartFactory)
    quantity = factory.Faker("random_int", min=1, max=10)

    cap = factory.SubFactory(CapFactory)
    shirt = factory.SubFactory(ShirtFactory)
