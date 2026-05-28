from django.urls import path
from .views import (
    CartClearView,
    CartDetailView,
    CartItemCreateView,
    CartItemDeleteView,
    CartItemUpdateView,
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("items/", CartItemCreateView.as_view(), name="item-create"),
    path("items/<int:pk>/", CartItemUpdateView.as_view(), name="item-update"),
    path("items/<int:pk>/delete", CartItemDeleteView.as_view(), name="item-delete"),
    path("clear/", CartClearView.as_view(), name="clear")
]

