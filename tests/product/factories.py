import factory
from factory.django import DjangoModelFactory

from iati_test.product.models import Cap, Material, Shirt, ShirtMaterialComposition
from iati_test.product.enums import SizeType


class MaterialFactory(DjangoModelFactory):
    class Meta:
        model = Material

    name = factory.Faker("word")


class ShirtFactory(DjangoModelFactory):
    class Meta:
        model = Shirt

    main_color = factory.Faker("color_name")
    secondary_color = factory.Faker("color_name")
    brand = factory.Faker("company")
    catalog_inclusion_date = factory.Faker("date_object")
    picture_url = factory.Faker("image_url")
    price_per_unit = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    initial_stock = factory.Faker("pyint", min_value=10)
    current_stock = factory.SelfAttribute("initial_stock")
    size = factory.Faker("word")
    size_type = factory.Iterator(SizeType.choices())
    sleeves = factory.Faker("boolean")

    @factory.post_generation
    def materials(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing
            return

        if extracted:
            # A list of materials was passed in, use them
            for material in extracted:
                ShirtMaterialCompositionFactory(shirt=self, material=material)
        else:
            # Create default materials
            for _ in range(3):  # Adjust the number of materials as needed
                ShirtMaterialCompositionFactory(shirt=self)


class ShirtMaterialCompositionFactory(DjangoModelFactory):
    class Meta:
        model = ShirtMaterialComposition

    shirt = factory.SubFactory(ShirtFactory)
    material = factory.SubFactory(MaterialFactory)
    percentage = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)


class CapFactory(DjangoModelFactory):
    class Meta:
        model = Cap

    main_color = factory.Faker("color_name")
    secondary_color = factory.Faker("color_name")
    brand = factory.Faker("company")
    catalog_inclusion_date = factory.Faker("date_object")
    picture_url = factory.Faker("image_url")
    price_per_unit = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    initial_stock = factory.Faker("pyint", min_value=10)
    current_stock = factory.SelfAttribute("initial_stock")
    logo_color = factory.Faker("color_name")
