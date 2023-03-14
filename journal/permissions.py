from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user.is_authenticated)

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool:
        return bool(obj.author == request.user)
