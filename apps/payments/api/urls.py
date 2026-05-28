from django.urls import path
from apps.payments.api.views import (
    CreatePaymentView,
    PaymentDetailView,
    PaymentListView,
)

app_name = "payments"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("create/", CreatePaymentView.as_view(), name="create"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="detail"),
]
