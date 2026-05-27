from rest_framework import viewsets, permissions, filters
from ..models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ProductDefaultPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.active.all()

    permission_classes = [permissions.AllowAny]
    pagination_class = ProductDefaultPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = ProductFilter

    search_fields = ['name', 'description']

    ordering_fields = ['price', 'crated_at', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
