from rest_framework.permissions import BasePermission

from apps.common.choices import UserRole

class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRole.ADMIN:
            return True
        
        return obj == request.user