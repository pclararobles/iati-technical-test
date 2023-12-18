# Generated by Django 5.0 on 2023-12-18 12:34

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0002_cap_deactivated_at_cap_is_active_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateField(default=datetime.date.today)),
                ("is_purchased", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Cart",
                "verbose_name_plural": "Carts",
                "db_table": "cart",
            },
        ),
        migrations.CreateModel(
            name="CartProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "cap",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.cap",
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.cart"
                    ),
                ),
                (
                    "shirt",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.shirt",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cart Product",
                "verbose_name_plural": "Cart Products",
                "db_table": "cart_product",
            },
        ),
        migrations.AddConstraint(
            model_name="cartproduct",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("cap__isnull", False), ("shirt__isnull", True)),
                    models.Q(("cap__isnull", True), ("shirt__isnull", False)),
                    _connector="OR",
                ),
                name="check_shirt_or_cap",
            ),
        ),
    ]