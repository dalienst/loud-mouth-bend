from rest_framework import serializers
from playlists.models import Song, Playlist


class SongSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=1)
    playlist = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Song
        fields = (
            "id",
            "name",
            "playlist",
        )
        read_only_fields = (
            "id",
            "playlist",
        )

    def create(self, validated_data):
        instance, _ = Song.objects.get_or_create(**validated_data)
        return instance


class PlaylistSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=1)
    tracks = serializers.SlugRelatedField(
        queryset=Song.objects.all(), slug_field="name", many=True
    )
    # tracklist = serializers.CharField(write_only=True)

    class Meta:
        model = Playlist
        fields = (
            "id",
            "name",
            "tracks",
            # "tracklist",
        )

    # def create(self, validated_data):
    #     tracklist = validated_data.pop("tracklist")
    #     playlist = super().get_or(validated_data)
    #     tracks = []
    #     for name in tracklist.split(","):
    #         track = Song.objects.get(name=name.strip())
    #         tracks.append(track)
    #     playlist.tracks.set(tracks)

    #     return playlist
