import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from iati_test.product.tasks import update_product_stock


def start():
    if settings.DEBUG:
        # Ensuring that the scheduler only runs in development
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_product_stock, "interval", hours=1)
        scheduler.start()
