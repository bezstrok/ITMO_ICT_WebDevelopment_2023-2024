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
