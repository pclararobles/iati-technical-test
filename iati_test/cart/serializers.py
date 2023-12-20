from datetime import date
from rest_framework import serializers

from iati_test.cart.models import Cart, CartProduct


class CartProductSerializer(serializers.Serializer):
    cap_id = serializers.IntegerField(required=False, allow_null=True)
    shirt_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(default=1)

    # Fields for GET request
    description = serializers.CharField(read_only=True)
    picture_url = serializers.CharField(read_only=True)
    price_per_unit = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    def validate(self, data) -> dict:
        """
        Check that shirt_id or cap_id is provided.
        """
        if not data.get("shirt_id") and not data.get("cap_id"):
            raise serializers.ValidationError("shirt_id or cap_id is required")
        if data.get("shirt_id") and data.get("cap_id"):
            raise serializers.ValidationError("only shirt_id or cap_id is required")

        return data

    def to_representation(self, instance) -> dict:
        """
        Add product fields to the response.
        """
        data = super().to_representation(instance)

        product = instance.product
        data["description"] = product.description
        data["picture_url"] = product.picture_url
        data["price_per_unit"] = product.price_per_unit

        return data


class PostCartSerializer(serializers.Serializer):
    products = CartProductSerializer(many=True)

    def save(self):
        """
        Update the cart products.
        """
        data = self.validated_data

        active_cart, _ = Cart.objects.get_or_create(is_purchased=False, date=date.today())

        for product in data["products"]:
            cap_id = product.get("cap_id")
            shirt_id = product.get("shirt_id")
            update_quantity = product.get("quantity")

            cart_product, _ = CartProduct.objects.get_or_create(
                cart=active_cart, cap_id=cap_id, shirt_id=shirt_id
            )

            if update_quantity > cart_product.product.current_stock:
                raise serializers.ValidationError(
                    f"Only {cart_product.product.current_stock} "
                    f"{cart_product.product.id} "
                    f"available in stock."
                )

            if update_quantity < 0 and abs(update_quantity) > cart_product.quantity:
                raise serializers.ValidationError(
                    f"Only {cart_product.quantity} "
                    f"{cart_product.product.id} "
                    f"available in the cart."
                )

            #: Update the cart product quantity
            cart_product.quantity = max(0, cart_product.quantity + update_quantity)
            cart_product.save()

            #: Update the stocks
            if update_quantity != 0:
                cart_product.product.current_stock = max(
                    0, cart_product.product.current_stock - update_quantity
                )
                cart_product.product.save()


class GetCartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "date", "products"]


class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    postal_address = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
