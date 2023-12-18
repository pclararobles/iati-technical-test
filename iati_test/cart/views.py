from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, views
from rest_framework.response import Response

from iati_test.cart.serializers import UpdateCartSerializer


class CartView(views.APIView):
    """
    View to add a product to the active cart.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["products"],
            properties={
                "products": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "cap_id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, description="Cap ID", format="int64"
                            ),
                            "shirt_id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, description="Shirt ID", format="int64"
                            ),
                            "update_quantity": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Update Quantity",
                                format="int32",
                            ),
                        },
                    ),
                )
            },
            example={
                "products": [
                    {"cap_id": 1, "shirt_id": None, "update_quantity": 2},
                    {"cap_id": None, "shirt_id": 3, "update_quantity": 1},
                ]
            },
        )
    )
    def post(self, request):
        input_serializer = UpdateCartSerializer(data=request.data)

        if input_serializer.is_valid(raise_exception=True):
            input_serializer.save()
            return Response({"message": "Product added to the cart."}, status=status.HTTP_200_OK)
