from rest_framework import serializers
from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "price",
            "quantity",
        )
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total_amount",
            "address",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CreateOrderSerializer(serializers.Serializer):
    address = serializers.CharField()

    def validate_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Address cannot be empty.")
        return value
