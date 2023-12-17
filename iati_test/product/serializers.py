from rest_framework import serializers

from iati_test.product.models import Cap, ProductMixin, Shirt, ShirtMaterialComposition


class ShirtMaterialCompositionSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source="material.name")

    class Meta:
        model = ShirtMaterialComposition
        fields = ("material_name", "percentage")


class ProductGenericSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductMixin
        exclude = ("initial_stock", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["id"].read_only = True
        self.fields["description"].read_only = True
        self.fields["deactivated_at"].read_only = True

        # In the catalog_inclusion_date should only be modified in the creation
        if self.instance:
            self.fields["catalog_inclusion_date"].read_only = True


class ShirtSerializer(ProductGenericSerializer):
    materials = ShirtMaterialCompositionSerializer(source="shirtmaterialcomposition_set", many=True)

    class Meta:
        model = Shirt
        fields = "__all__"


class CapSerializer(ProductGenericSerializer):
    class Meta:
        model = Cap
        fields = "__all__"


class ProductSerializer(serializers.Serializer):
    caps = CapSerializer(many=True)
    shirts = ShirtSerializer(many=True)
