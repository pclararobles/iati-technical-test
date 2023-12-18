import factory
from factory.django import DjangoModelFactory
from datetime import date
from iati_test.cart.models import Cart


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    date = factory.LazyFunction(date.today)
    is_purchased = False
