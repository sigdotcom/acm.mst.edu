from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission which only allows admins to edit data
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission which only allows Owners to edit data

    Requires that the Model/Serializer has field email.

    TODO: Make it so that it does not require there to be email.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.email == obj.email
