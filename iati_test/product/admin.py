from django.contrib import admin

from iati_test.product.models import Cap, Material, Shirt, ShirtMaterialComposition


class ShirtMaterialCompositionInline(admin.TabularInline):
    model = ShirtMaterialComposition
    extra = 1


class ShirtAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "main_color",
        "size",
        "price_per_unit",
        "current_stock",
        "catalog_inclusion_date",
        "description",
    )
    list_filter = ("brand", "size_type", "sleeves")
    inlines = [ShirtMaterialCompositionInline]
    search_fields = ("brand", "main_color", "size")

    def get_readonly_fields(self, request, obj=None):
        """
        If the object already exists, the initial stock cannot be modified.
        """
        if obj is not None:
            return self.readonly_fields + ("initial_stock",)
        return self.readonly_fields


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class CapAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "main_color",
        "price_per_unit",
        "current_stock",
        "catalog_inclusion_date",
        "description",
    )
    list_filter = ("brand",)
    search_fields = ("brand", "main_color")

    def get_readonly_fields(self, request, obj=None):
        """
        If the object already exists, the initial stock cannot be modified.
        """
        if obj is not None:
            return self.readonly_fields + ("initial_stock",)
        return self.readonly_fields


admin.site.register(Shirt, ShirtAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Cap, CapAdmin)
