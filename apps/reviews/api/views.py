from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.reviews.models import Review
from apps.reviews.api.serializers import ReviewSerializer, CreateReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReviewSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
