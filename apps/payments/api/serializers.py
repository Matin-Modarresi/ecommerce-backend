from rest_framework import serializers
from apps.orders.models import Order
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id", read_only=True)
    order_status = serializers.CharField(source="order.status", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "order_id",
            "order_status",
            "amount",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate_order_id(self, value):
        try:
            order = Order.objects.get(id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order does not exist.")

        self.order = order
        return value

    def validate(self, attrs):
        order = getattr(self, "order", None)
        if order is None:
            return attrs

        request = self.context["request"]
        if order.user != request.user:
            raise serializers.ValidationError("You do not have permission to pay for this order.")

        if hasattr(order, "payments") and order.payments.filter(status="success").exists():
            raise serializers.ValidationError("This order is already paid.")

        return attrs
