from django.urls import path

from iati_test.product.views import CapViewSet, ProductsAPIView, ShirtViewSet


urlpatterns = [
    path("", ProductsAPIView.as_view(), name="products-list"),
    path("caps/", CapViewSet.as_view({"get": "list", "post": "create"}), name="cap-list"),
    path(
        "caps/<int:pk>/",
        CapViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="cap-detail",
    ),
    path("shirts/", ShirtViewSet.as_view({"get": "list", "post": "create"}), name="shirt-list"),
    path(
        "shirts/<int:pk>/",
        ShirtViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="shirt-detail",
    ),
]
