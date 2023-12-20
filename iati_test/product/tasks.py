from django.db import models

from iati_test.cart.models import CartProduct
from iati_test.product.models import Cap, Shirt


def update_product_stock():
    # Update stock for Caps
    for cap in Cap.objects.all():
        used_stock_quantity = (
            CartProduct.objects.filter(cap=cap, quantity__gt=0).aggregate(
                total_used=models.Sum("quantity")
            )["total_used"]
            or 0
        )

        cap.current_stock = cap.initial_stock - used_stock_quantity
        cap.save()

    # Update stock for Shirts
    for shirt in Shirt.objects.all():
        used_stock_quantity = (
            CartProduct.objects.filter(shirt=shirt, quantity__gt=0).aggregate(
                total_used=models.Sum("quantity")
            )["total_used"]
            or 0
        )

        shirt.current_stock = shirt.initial_stock - used_stock_quantity
        shirt.save()
