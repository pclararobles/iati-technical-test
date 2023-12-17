from rest_framework import serializers

from iati_test.product.models import Cap, Shirt, ShirtMaterialComposition


class ShirtMaterialCompositionSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source="material.name")

    class Meta:
        model = ShirtMaterialComposition
        fields = ("material_name", "percentage")


class ShirtSerializer(serializers.ModelSerializer):
    materials = ShirtMaterialCompositionSerializer(source="shirtmaterialcomposition_set", many=True)

    class Meta:
        model = Shirt
        exclude = ("current_stock", "created_at", "updated_at")


class CapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cap
        exclude = ("current_stock", "created_at", "updated_at")


class ProductSerializer(serializers.Serializer):
    caps = CapSerializer(many=True)
    shirts = ShirtSerializer(many=True)
