from rest_framework import serializers
from ..models import Product, ProductImage, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'average_rating', 'review_count']


class ProductDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'average_rating', 'review_count', 'slug']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    سریالایزر مخصوص ایجاد و ویرایش محصول.
    فیلدهای محاسباتی و خودکار در اینجا read_only هستند.
    """

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'description',
            'price', 'stock_quantity', 'is_active'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("قیمت محصول باید بیشتر از صفر باشد.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("موجودی انبار نمی‌تواند عدد منفی باشد.")
        return value