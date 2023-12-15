from django.db import models
from django.utils import timezone

from iati_test.core.models import TimeStampedModelMixin
from iati_test.product.enums import SizeType


class ProductMixin(TimeStampedModelMixin):
    """
    An abstract base class model that provides the base fields for any kind of
    product.
    """

    main_color = models.CharField(max_length=255)
    secondary_color = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    catalog_inclusion_date = models.DateField(default=timezone.now, editable=False)
    picture_url = models.URLField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    initial_stock = models.IntegerField(editable=False)
    current_stock = models.IntegerField()
    description = models.TextField()

    class Meta:
        abstract = True


class Shirt(ProductMixin):
    """
    A model containing all data relevant for a shirt product.
    """

    size = models.CharField(max_length=255)
    size_type = models.CharField(max_length=255, choices=SizeType.choices())
    sleeves = models.BooleanField()
    materials = models.ManyToManyField("product.Material", through="product.ShirtCompostion")

    class Meta:
        verbose_name = "Shirt"
        verbose_name_plural = "Shirts"
        db_table = "shirt"

    def save(self, *args, **kwargs):
        """
        Overwritten save method to update the description field.
        """
        super(Shirt, self).save(*args, **kwargs)

        material_descriptions = []
        for composition in self.shirtcomposition_set.all():
            material_descriptions.append(f"{composition.material.name} ({composition.percentage}%)")

        self.description = (
            "This is a shirt. "
            f"Brand: {self.brand}. "
            f"Main Color: {self.main_color}. "
            f"Secondary Color: {self.secondary_color}. "
            f"Catalog Inclusion Date: {self.catalog_inclusion_date}. "
            f"Size: {self.size}. "
            f"Size Type: {self.size_type}. "
            f"Composition: {', '.join(material_descriptions)}. "
        )

        super(Shirt, self).save(*args, **kwargs, update_fields=["description"])


class Material(models.Model):
    """
    A model containing all possible materials for a shirt.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Shirt Material"
        verbose_name_plural = "Shirt Materials"
        db_table = "shirt_material"

    def __str__(self):
        return self.name


class ShirtCompostion(TimeStampedModelMixin):
    """
    A model containing the material composition of a shirt.
    """

    shirt = models.ForeignKey("product.Shirt", on_delete=models.PROTECT)
    material = models.ForeignKey("product.Material", on_delete=models.PROTECT)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Shirt Composition"
        verbose_name_plural = "Shirt Compositions"
        db_table = "shirt_composition"


class Cap(ProductMixin):
    """
    A model containing all data relevant for a cap product.
    """

    logo_color = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Cap"
        verbose_name_plural = "Caps"
        db_table = "cap"

    def save(self, *args, **kwargs):
        self.description = (
            "This is a shirt."
            f"Brand: {self.brand}. "
            f"Main Color: {self.main_color}. "
            f"Secondary Color: {self.secondary_color}. "
            f"Catalog Inclusion Date: {self.catalog_inclusion_date}. "
        )

        super(ProductMixin, self).save(*args, **kwargs)
