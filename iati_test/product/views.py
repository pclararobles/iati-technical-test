from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from iati_test.product.models import Cap, Shirt
from iati_test.product.serializers import ProductSerializer


class ProductsAPIView(APIView):
    @swagger_auto_schema(
        responses={
            200: ProductSerializer(),
        },
    )
    def get(self, request, format=None):
        shirts = Shirt.objects.all().order_by("catalog_inclusion_date")
        caps = Cap.objects.all().order_by("catalog_inclusion_date")

        serializer = ProductSerializer({"shirts": shirts, "caps": caps})
        return Response(serializer.data)
