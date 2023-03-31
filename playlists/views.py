from rest_framework import viewsets

from playlists.serializers import (
    SongSerializer,
    PlaylistSerializer,
    MovieSerializer,
    GenreSerializer,
    RecommendationSerializer,
    DailyRecommendationSerializer
)
from playlists.models import Song, Playlist, Movie, Genre, Recommendation, DailyRecommendation


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

class DailyRecommendationViewSet(viewsets.ModelViewSet):
    queryset = DailyRecommendation.objects.all()
    serializer_class = DailyRecommendationSerializer
    lookup_field = "genre"