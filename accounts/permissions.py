from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        return bool(obj == request.user)


class MeUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)
