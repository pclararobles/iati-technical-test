from rest_framework import serializers

from iati_test.product.models import Cap, Material, ProductMixin, Shirt, ShirtMaterialComposition


class ShirtMaterialCompositionSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source="material.name")

    class Meta:
        model = ShirtMaterialComposition
        fields = ("material_name", "percentage")


class ProductGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMixin
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Define field particularities for the ProductMixin serializer.
        """
        super().__init__(*args, **kwargs)

        if self.instance is not None or self.context.get("many"):
            self.removed_fields = ["initial_stock", "created_at", "updated_at"]
        else:
            self.removed_fields = ["created_at", "updated_at"]

        for field_name in self.removed_fields:
            self.fields.pop(field_name, None)

        self.fields["id"].read_only = True
        self.fields["description"].read_only = True
        self.fields["deactivated_at"].read_only = True

        if self.instance:
            self.fields["catalog_inclusion_date"].read_only = True

    def validate(self, attrs):
        """
        Custom validation to check for fields that shouldn't be updated.
        """
        if self.instance is not None and self.context.get("many", False) is False:
            # Check if any of the removed fields are present in the update
            for field in self.removed_fields:
                if field in self.initial_data:
                    raise serializers.ValidationError(
                        {field: "Updating this field is not allowed."}
                    )

        return super().validate(attrs)


class ShirtSerializer(ProductGenericSerializer):
    materials = ShirtMaterialCompositionSerializer(source="shirtmaterialcomposition_set", many=True)

    class Meta:
        model = Shirt
        fields = "__all__"

    def create(self, validated_data) -> Shirt:
        """
        Overwritten create method to handle the M2M relationships.
        """
        materials_data = validated_data.pop("shirtmaterialcomposition_set", [])

        shirt = Shirt.objects.create(**validated_data)

        for material_data in materials_data:
            material = Material.objects.get(name=material_data["material"]["name"])
            ShirtMaterialComposition.objects.create(
                shirt=shirt, material=material, percentage=material_data["percentage"]
            )

        return shirt


class CapSerializer(ProductGenericSerializer):
    class Meta:
        model = Cap
        fields = "__all__"


class ProductSerializer(serializers.Serializer):
    caps = CapSerializer(many=True, context={"many": True})
    shirts = ShirtSerializer(many=True, context={"many": True})
