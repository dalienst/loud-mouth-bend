from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import (
    UserRegister,
    EditorRegister,
    LogoutView,
    ProfileListView,
    ProfileDetailView,
    UserView,
    UserDetailView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path("register/editor/", EditorRegister.as_view(), name="editor-register"),
    path("me/<str:id>/", UserDetailView.as_view(), name="me-detail"),
    path("profile/<str:user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
]
