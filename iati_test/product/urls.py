from django.urls import path

from iati_test.product.views import ProductsAPIView


urlpatterns = [
    path("", ProductsAPIView.as_view(), name="products-list"),
]
