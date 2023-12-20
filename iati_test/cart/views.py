from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, views
from rest_framework.response import Response

from iati_test.cart.models import Cart
from iati_test.cart.serializers import CustomerSerializer, GetCartSerializer, PostCartSerializer


class CartView(views.APIView):
    """
    View with main actions related to a cart.
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
                            "quantity": openapi.Schema(
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
    def post(self, request) -> Response:
        input_serializer = PostCartSerializer(data=request.data)

        if input_serializer.is_valid(raise_exception=True):
            input_serializer.save()
            return Response({"message": "Product added to the cart."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: GetCartSerializer()})
    def get(self, request) -> Response:
        """
        Get the active cart.
        """
        active_cart, _ = Cart.objects.get_or_create(is_purchased=False, date=date.today())

        return Response(GetCartSerializer(active_cart).data, status=status.HTTP_200_OK)


class PurchaseView(views.APIView):
    """
    View to purchase the active cart.
    """

    def post(self, request, *args, **kwargs) -> Response:
        serializer = CustomerSerializer(data=request.data)

        try:
            active_cart = Cart.objects.get(is_purchased=False, date=date.today())
        except Cart.DoesNotExist:
            return Response({"message": "No active cart found"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid(raise_exception=True):
            email_content = render_to_string("purchase_summary.txt", serializer.validated_data)

            send_mail(
                subject="Purchase Summary",
                message=email_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.validated_data["email"]],
                fail_silently=False,
            )

            active_cart.is_purchased = True
            active_cart.save()
            return Response({"message": "Purchase successful and email sent"})
