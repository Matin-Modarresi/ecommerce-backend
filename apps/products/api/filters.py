from django_filters import rest_framework as filters
from ..models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_slug = filters.CharFilter(field_name="category__slug")

    class Meta:
        model = Product
        fields = ['category_slug', 'min_price', 'max_price']

