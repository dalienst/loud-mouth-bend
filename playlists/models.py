from django.db import models
from accounts.abstracts import TimeStampedModel, UniversalIdModel


class Song(TimeStampedModel, UniversalIdModel):
    name = models.CharField(max_length=400)

    def __str__(self) -> str:
        return self.name


class Playlist(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=400, blank=False, null=False, default="")
    tracks = models.ManyToManyField(Song, related_name="playlist")

    def __str__(self) -> str:
        return self.name


class Movie(TimeStampedModel, UniversalIdModel):
    name = models.CharField(max_length=400)

    def __str__(self) -> str:
        return self.name


class Genre(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=400)

    def __str__(self) -> str:
        return self.name


class Recommendation(UniversalIdModel, TimeStampedModel):
    day = models.CharField(max_length=400)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre")
    movies = models.ManyToManyField(Movie, related_name="movies")


class DailyRecommendation(UniversalIdModel, TimeStampedModel):
    genre = models.OneToOneField(Genre, on_delete=models.CASCADE)
    day = models.CharField(max_length=400, blank=False, null=False, default="")
    movies = models.ManyToManyField(Movie, related_name="movies_of_the_day")

    def __str__(self) -> str:
        return self.day
