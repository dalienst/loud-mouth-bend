from rest_framework.routers import DefaultRouter

from playlists.views import (
    SongViewSet,
    PlaylistViewSet,
)

router = DefaultRouter()
router.register(r"song", SongViewSet, basename="song"),
router.register(r"playlist", PlaylistViewSet, basename="playlist"),

urlpatterns = router.urls
