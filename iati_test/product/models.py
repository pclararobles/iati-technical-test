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
    catalog_inclusion_date = models.DateField(default=timezone.now)
    picture_url = models.URLField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    initial_stock = models.IntegerField()
    current_stock = models.IntegerField()
    description = models.TextField(blank=True, editable=False)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """
        Store the initial stock in a separate variable to be able to check if
        it is being modified.
        """
        super().__init__(*args, **kwargs)

        self._initial_initial_stock = self.initial_stock

    def save(self, *args, **kwargs):
        """
        Overwritten save method to raise an error if the initial stock is being
        modified.
        """
        if self.pk is not None and self.initial_stock != self._initial_initial_stock:
            raise ValueError("The initial stock cannot be modified.")

        super(ProductMixin, self).save(*args, **kwargs)


class Shirt(ProductMixin):
    """
    A model containing all data relevant for a shirt product.
    """

    size = models.CharField(max_length=255)
    size_type = models.CharField(max_length=255, choices=SizeType.choices())
    sleeves = models.BooleanField()
    materials = models.ManyToManyField(
        "product.Material", through="product.ShirtMaterialComposition"
    )

    class Meta:
        verbose_name = "Shirt"
        verbose_name_plural = "Shirts"
        db_table = "shirt"

    def save(self, *args, **kwargs):
        """
        Overwritten save method to update the description field.
        """
        super(Shirt, self).save(*args, **kwargs)

        material_descriptions = [
            f"{composition.material.name} ({composition.percentage}%)"
            for composition in self.shirtmaterialcomposition_set.all()
        ]

        new_description  = (
            "This is a shirt. "
            f"Brand: {self.brand}. "
            f"Main Color: {self.main_color}. "
            f"Secondary Color: {self.secondary_color}. "
            f"Catalog Inclusion Date: {self.catalog_inclusion_date}. "
            f"Size: {self.size}. "
            f"Size Type: {self.size_type}. "
            f"Composition: {', '.join(material_descriptions)}. "
        )

        if not self.pk:
            self.description = new_description
            super(Shirt, self).save(*args, **kwargs)
        else:
            if self.description != new_description:
                self.description = new_description
                kwargs["force_insert"] = False
                super(Shirt, self).save(*args, **kwargs, update_fields=["description"])
            else:
                super(Shirt, self).save(*args, **kwargs)


class Material(models.Model):
    """
    A model containing all possible materials for a shirt.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        db_table = "material"

    def __str__(self):
        return self.name


class ShirtMaterialComposition(TimeStampedModelMixin):
    """
    A model containing the material composition of a shirt.
    """

    shirt = models.ForeignKey("product.Shirt", on_delete=models.PROTECT)
    material = models.ForeignKey("product.Material", on_delete=models.PROTECT)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Shirt Material Composition"
        verbose_name_plural = "Shirt Material Compositions"
        db_table = "shirt_material_composition"


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
