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
    EditorDetailView,
    EditorView,
    AdminRegister,
    AdminDetailView,
    AdminView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path("register/editor/", EditorRegister.as_view(), name="editor-register"),
    path("register/admin/", AdminRegister.as_view(), name="admin-register"),
    path("me/<str:id>/", UserDetailView.as_view(), name="me-detail"),
    path("editor/<str:id>/", EditorDetailView.as_view(), name="editor-detail"),
    path("editors/", EditorView.as_view(), name="editors"),
    path("admin/<str:id>/", AdminDetailView.as_view(), name="admin-detail"),
    path("admins/", AdminView.as_view(), name="admins"),
    path("profile/<str:user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
]
