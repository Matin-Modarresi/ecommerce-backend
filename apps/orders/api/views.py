from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    CreateOrderSerializer,
    OrderSerializer,
)
from apps.orders.models import Order
from apps.orders.services import create_order_from_cart
from apps.core.permissions import IsStaffOrSuperuser


class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.prefetch_related("items")

        if request.user.is_staff or request.user.is_superuser:
            orders = queryset.all()
        else:
            orders = queryset.filter(user=request.user)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.prefetch_related("items").get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not (request.user.is_staff or request.user.is_superuser or order.user_id == request.user.id):
            return Response(
                {"detail": "You do not have permission to access this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.validated_data["address"]

        order = create_order_from_cart(
            user=request.user,
            cart=request.user.cart,
            address=address,
        )

        output_serializer = OrderSerializer(order)
        return Response(
            {
                "message": "Order created successfully.",
                "order": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
