from apps.users.models import User
from apps.common.choices import UserRole
from rest_framework.permissions import BasePermission,IsAuthenticated
from apps.common.choices import OrderStatus


class IsADMIN(IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super().has_permission(request,view)
        return is_auth and request.user.role == UserRole.ADMIN
    



class CanUpdateOrderStatus(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):

        user = request.user
        new_status = request.data.get("status")

        if user.role == UserRole.ADMIN:
            return True

        if user.role == UserRole.WAITER:

            transitions = {
                OrderStatus.PENDING: [
                    OrderStatus.PREPARING,
                    OrderStatus.CANCELED
                ],

                OrderStatus.PREPARING: [
                    OrderStatus.READY
                ],
                OrderStatus.PREPARING: [
                    OrderStatus.DELIVERING
                ],
                OrderStatus.DELIVERING: [
                    OrderStatus.DONE
                ]
            }

            return new_status in transitions.get(obj.status, [])

        if user.role == UserRole.DELIVERER:

            transitions = {
                OrderStatus.READY: [
                    OrderStatus.DELIVERING
                ],

                OrderStatus.DELIVERING: [
                    OrderStatus.DONE
                ]
            }

            return new_status in transitions.get(obj.status, [])
        
        if user.role == UserRole.CLIENT:

            transitions = {
                OrderStatus.PENDING: [
                    OrderStatus.CANCELED
                ],


            }

            return new_status in transitions.get(obj.status, [])
        
        return False
