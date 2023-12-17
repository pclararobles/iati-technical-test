from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from iati_test.product.models import Cap, Shirt
from iati_test.product.serializers import CapSerializer, ProductSerializer


class ProductsAPIView(APIView):
    """
    Class containing the logic for actions related to all products.
    """

    @swagger_auto_schema(
        responses={
            200: ProductSerializer(),
        },
    )
    def get(self, request, format=None):
        shirts = Shirt.objects.filter(is_active=True).order_by("catalog_inclusion_date").all()
        caps = Cap.objects.filter(is_active=True).order_by("catalog_inclusion_date").all()

        serializer = ProductSerializer({"shirts": shirts, "caps": caps})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Generic viewset for any kind of product.
    """

    def get_queryset(self):
        return self.queryset.filter(is_active=True).order_by("catalog_inclusion_date").all()


class CapViewSet(ProductViewSet):
    """
    Viewset for cap model.
    """

    queryset = Cap.objects.all()
    serializer_class = CapSerializer


class ShirtViewSet(ProductViewSet):
    """
    Viewset for shirt model.
    """

    queryset = Shirt.objects.all()
    serializer_class = CapSerializer
