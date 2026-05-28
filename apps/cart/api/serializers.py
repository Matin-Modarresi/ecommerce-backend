from rest_framework import serializers
from ..models import Cart, CartItem
from apps.products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.title", read_only=True)
    unit_price = serializers.BigIntegerField(source="product.price", read_only=True, min_value=0)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "total_price",
        )
        read_only_fields = (
            "id",
            "product_name",
            "unit_price",
            "total_price",
        )

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cartitem_set", many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "id",
            "items",
            "total_items",
            "total_price",
        )
        read_only_fields = fields

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.cartitem_set.all())

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.cartitem_set.all())


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate(self, attrs):
        product = Product.objects.get(id=attrs["product_id"])
        quantity = attrs["quantity"]

        if product.stock < quantity:
            raise serializers.ValidationError("Not enough stock available.")

        attrs["product"] = product
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        quantity = attrs["quantity"]
        instance = self.instance
        product = instance.product

        if product.stock < quantity:
            raise serializers.ValidationError("Not enough stock available.")

        return attrs
