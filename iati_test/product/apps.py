import sys
from django.apps import AppConfig
from django.conf import settings


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "iati_test.product"
    verbose_name = "Product"

    def ready(self):
        # Upload the base data only in development
        if settings.DEBUG and "manage.py" not in sys.argv and "pytest" not in sys.modules:
            from iati_test.product.fixtures.product_base_data import ProductsBaseData

            ProductsBaseData.upload_data()

        # Execute the scheduler only in development
        if settings.DEBUG:
            from iati_test.product import scheduler

            scheduler.start()
