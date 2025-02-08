from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a product to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the product
        return obj.user == request.user
