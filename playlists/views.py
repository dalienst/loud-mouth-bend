from rest_framework import viewsets

from playlists.serializers import (
    SongSerializer,
    PlaylistSerializer,
)
from playlists.models import Song, Playlist


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
