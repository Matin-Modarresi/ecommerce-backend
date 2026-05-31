from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.orders.models import Order
from apps.payments.api.serializers import (
    CreatePaymentSerializer,
    PaymentSerializer,
)
from apps.payments.models import Payment, PaymentStatus


class PaymentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            payments = Payment.objects.select_related("order").all()
        else:
            payments = Payment.objects.select_related("order").filter(order__user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            payment = Payment.objects.select_related("order").get(pk=pk)
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, payment)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        order = serializer.order

        if order.total_amount <= 0:
            return Response(
                {"detail": "Invalid order amount."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            status=PaymentStatus.PENDING,
        )

        output_serializer = PaymentSerializer(payment)
        return Response(
            {
                "message": "Payment created successfully.",
                "payment": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
