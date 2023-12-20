from django.urls import path

from iati_test.cart.views import CartView, PurchaseView


urlpatterns = [
    path("", CartView.as_view(), name="cart-view"),
    path("purchase/", PurchaseView.as_view(), name="purchase"),
]
