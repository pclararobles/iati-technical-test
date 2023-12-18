from django.db import models
from datetime import date

from iati_test.core.models import TimeStampedModelMixin
from iati_test.product.models import ProductMixin


class Cart(TimeStampedModelMixin):
    """
    Model containing the cart information.
    """

    date = models.DateField(default=date.today)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        db_table = "cart"


class CartProduct(TimeStampedModelMixin):
    """
    Model containing the cart product information.
    """

    cart = models.ForeignKey("cart.Cart", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    cap = models.ForeignKey("product.Cap", on_delete=models.PROTECT, null=True)
    shirt = models.ForeignKey("product.Shirt", on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "Cart Product"
        verbose_name_plural = "Cart Products"
        db_table = "cart_product"
        constraints = [
            models.CheckConstraint(
                check=models.Q(shirt__isnull=True, cap__isnull=False)
                | models.Q(shirt__isnull=False, cap__isnull=True),
                name="check_shirt_or_cap",
            )
        ]

    @property
    def product(self) -> ProductMixin:
        """
        Return the relevant product.
        """
        if self.shirt:
            return self.shirt

        return self.cap
