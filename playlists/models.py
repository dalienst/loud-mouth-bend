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


class MovieStore(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=400)
    movies = models.ManyToManyField(Movie, related_name="moviestore")

    def __str__(self) -> str:
        return self.name

