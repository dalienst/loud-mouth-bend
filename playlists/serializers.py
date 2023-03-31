from rest_framework import serializers
from playlists.models import (
    Song,
    Playlist,
    Movie,
    Genre,
    Recommendation,
    DailyRecommendation,
)
from rest_framework.validators import UniqueValidator


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


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        min_length=1, validators=[UniqueValidator(Movie.objects.all())]
    )
    movies_of_the_day = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "name",
            "movies_of_the_day",
        )


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        min_length=1, validators=[UniqueValidator(Genre.objects.all())]
    )

    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        genre = Genre.objects.create(**validated_data)
        genre.save()
        DailyRecommendation.objects.create(genre=genre)
        return genre


class DailyRecommendationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    genre = serializers.CharField(source="genre.name", read_only=True)
    day = serializers.CharField(min_length=1)
    movies = serializers.SlugRelatedField(
        many=True, queryset=Movie.objects.all(), slug_field="name"
    )

    class Meta:
        model = DailyRecommendation
        fields = (
            "id",
            "genre",
            "day",
            "movies",
        )
        read_only_fields = (
            "id",
            "genre",
        )


class RecommendationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    day = serializers.CharField(min_length=1)
    movies = serializers.SlugRelatedField(
        many=True, queryset=Movie.objects.all(), slug_field="name"
    )

    class Meta:
        model = Recommendation
        fields = (
            "id",
            "day",
            "genre",
            "movies",
        )
