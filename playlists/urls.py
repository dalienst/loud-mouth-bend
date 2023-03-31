from rest_framework.routers import DefaultRouter

from playlists.views import (
    SongViewSet,
    PlaylistViewSet,
    MovieViewSet,
    GenreViewSet,
    RecommendationViewSet,
    DailyRecommendationViewSet,
)

router = DefaultRouter()
router.register(r"song", SongViewSet, basename="song"),
router.register(r"playlist", PlaylistViewSet, basename="playlist"),
router.register(r"movie", MovieViewSet, basename="movie"),
router.register(r"genre", GenreViewSet, basename="genre"),
router.register(r"recommend", RecommendationViewSet, basename="recommend"),
router.register(r"daily", DailyRecommendationViewSet, basename="daily"),

urlpatterns = router.urls
