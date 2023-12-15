from django.contrib import admin

from iati_test.product.models import Cap, Material, Shirt, ShirtCompostion


class ShirtCompositionInline(admin.TabularInline):
    model = ShirtCompostion
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
    inlines = [ShirtCompositionInline]
    search_fields = ("brand", "main_color", "size")


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


admin.site.register(Shirt, ShirtAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Cap, CapAdmin)
