from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        return bool(obj == request.user)


class MeUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)


class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view: APIView):
        return bool(request.user.is_editor)

    def has_object_permission(self, request, view, obj):
        return bool(obj.editor == request.user)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view: APIView):
        return bool(request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return bool(obj.created_by == request.user)