from rest_framework.permissions import BasePermission


class IsStaffOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or request.user.is_superuser)
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    فقط مالک آبجکت می‌تواند ویرایش/حذف کند.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.user == request.user or obj.owner == request.user


class IsAuthenticatedForWrite(BasePermission):
    """
    برای create/update/delete فقط کاربر لاگین‌شده.
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(request.user and request.user.is_authenticated)


def IsInGroup(group_name: str):
    class _IsInGroup(BasePermission):
        def has_permission(self, request, view):
            user = request.user
            return bool(
                user
                and user.is_authenticated
                and user.groups.filter(name=group_name).exists()
            )

    return _IsInGroup


class IsOwnerOrStaff(BasePermission):
    """
    اجازه دسترسی فقط به مالک شیء یا کارمند/ادمین.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user and (user.is_staff or user.is_superuser):
            return True

        if hasattr(obj, "order"):
            return obj.order.user.id == user.id

        return False


class IsOwner(BasePermission):
    """
    فقط مالک آبجکت (بدون استثناء staff/superuser).
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user.id == request.user.id

        return False
