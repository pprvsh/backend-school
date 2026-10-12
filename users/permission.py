
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAdminUser,
)


class IsAdminUserOrReadOnly(IsAdminUser):
    """
    Anyone can read.
    Only staff users can modify.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class AdmissionsPermission(BasePermission):
    """
    Anyone can submit an admission inquiry.
    Only staff users can view, update, or delete inquiries.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
