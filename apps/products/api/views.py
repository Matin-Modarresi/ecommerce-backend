from rest_framework import viewsets, permissions, filters
from ..models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ProductDefaultPagination
from apps.core.permissions import IsStaffOrSuperuser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    # permission_classes = [permissions.AllowAny]
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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list":
            return Product.active.all()
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        # برای اکشن‌های create, update, partial_update از سریالایزر جدید استفاده می‌کنیم
        return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsStaffOrSuperuser]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        """
        به جای حذف فیزیکی، می‌توان محصول را غیرفعال کرد (Soft Delete).
        اگر بیزنس مدل شما حذف فیزیکی است، این متد را نادیده بگیرید.
        """
        instance.is_active = False
        instance.save()
