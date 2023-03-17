from news.models import NewsArticle, Newspaper, NewsArticleCategory
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer, EditorSerializer


class NewsPaperSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=10)
    tagline = serializers.CharField(min_length=10)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Newspaper
        fields = (
            "id",
            "name",
            "tagline",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class NewsArticleCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=2)
    tagline = serializers.CharField(min_length=2)

    class Meta:
        model = NewsArticleCategory
        fields = (
            "id",
            "name",
            "tagline",
        )
        read_only_fields = ("id",)


class NewsArticleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    read_time = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(
        max_length=400,
        min_length=10,
    )
    subtitle = serializers.CharField(
        max_length=1000,
        min_length=10,
    )
    image = serializers.ImageField(use_url=True, required=False)
    body = serializers.CharField(
        min_length=10,
    )
    slug = serializers.SlugField(read_only=True)
    # editor = EditorSerializer(read_only=True)
    editor = serializers.CharField(source="editor.username", read_only=True)

    class Meta:
        model = NewsArticle
        fields = (
            "id",
            "read_time",
            "created_at",
            "title",
            "subtitle",
            "image",
            "body",
            "slug",
            "editor",
            "is_mainstory",
        )
        read_only_fields = (
            "id",
            "read_time",
            "created_at",
            "slug",
            "editor",
            "is_mainstory",
        )
