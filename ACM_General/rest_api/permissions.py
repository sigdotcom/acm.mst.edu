from rest_framework import permissions


class IsStaffOrReadonly(permissions.BasePermission):
    """
    Allows only staff members, classified by the `is_staff` method of the User
    model, to have complete permissions if they are logged in. Otherwise, the
    Users can only perform the safe methods of GET, HEAD, or OPTIONS.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_staff
