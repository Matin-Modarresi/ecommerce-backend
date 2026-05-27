from rest_framework import viewsets, permissions
from ..models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.active.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
