from django.urls import path

from iati_test.cart.views import CartView


urlpatterns = [
    path("", CartView.as_view(), name="cart-view"),
]
