from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.notifications.api.serializers import (
    NotificationCreateSerializer,
    NotificationSerializer,
)
from apps.notifications.models import Notification
from apps.core.permissions import IsOwner, IsOwnerOrStaff


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    def get_permissions(self):
        # retrieve -> فقط مالک یا ادمین
        if self.action == "retrieve":
            return [permissions.IsAuthenticated(), IsOwnerOrStaff()]

        # mark as read -> فقط مالک (حتی ادمین هم اگر مالک نباشد ممنوع)
        if self.action == "mark_as_read":
            return [permissions.IsAuthenticated(), IsOwner()]

        # سایر اکشن‌ها (list, mark_all_as_read, create, ...)
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return NotificationCreateSerializer
        return NotificationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"], url_path="mark-as-read")
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read", "updated_at"])
        return Response(
            {"detail": "Notification marked as read."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["patch"], url_path="mark-all-as-read")
    def mark_all_as_read(self, request):
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(
            {
                "detail": "All notifications marked as read.",
                "updated_count": updated_count,
            },
            status=status.HTTP_200_OK,
        )
