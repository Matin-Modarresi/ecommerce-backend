from django.urls import path
from apps.orders.api.views import (
    CreateOrderView,
    OrderDetailView,
    OrderListView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("create/", CreateOrderView.as_view(), name="create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
]
