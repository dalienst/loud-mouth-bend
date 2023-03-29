from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (
    UserSerializer,
    LogoutSerializer,
    ProfileSerializer,
    EditorSerializer,
    AdminSerializer,
)
from accounts.models import Profile
from accounts.permissions import IsUser, MeUser

User = get_user_model()


class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = "id"
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsUser,
    ]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EditorRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = EditorSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class EditorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditorSerializer
    lookup_field = "id"
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsUser,
    ]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {"message": "Editor deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EditorView(generics.ListAPIView):
    serializer_class = EditorSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(is_editor=True)


class AdminRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = AdminSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminSerializer
    lookup_field = "id"
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsUser,
    ]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {"message": "Editor deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class AdminView(generics.ListAPIView):
    serializer_class = AdminSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(is_admin=True)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):  # type:ignore[no-untyped-def]
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        MeUser,
    )
    serializer_class = ProfileSerializer
    lookup_field = "user"
    queryset = Profile.objects.all()


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
