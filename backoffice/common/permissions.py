from rest_framework import permissions


class IsOwnerShopOnlyOrGetOnly(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        print(request.user)
        return True
        # return obj.store_id == request.user.store_id


class IsOnlySuperUser(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        return request.user.is_superuser
