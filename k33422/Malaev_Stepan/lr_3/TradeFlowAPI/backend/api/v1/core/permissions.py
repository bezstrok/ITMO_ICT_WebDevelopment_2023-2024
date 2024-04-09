from rest_framework.permissions import BasePermission


class IsUserRoleObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUserManufacturer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manufacturer


class IsUserManufacturerObject(IsUserManufacturer, BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.manufacturer == request.user.manufacturer


class IsUserManufacturerNestedProduct(IsUserManufacturer, BasePermission):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            product_obj = view.get_product()
            return product_obj.manufacturer == request.user.manufacturer
        
        return False


class IsProductBatchAvailable(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_available


class IsUserBroker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_broker


class IsUserBrokerObject(IsUserBroker, BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.broker == request.user.broker


class IsTradeChangeable(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.is_closed


class IsTradeProductBatchAvailable(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.product_batch.is_available
