from news.models import (
    NewsArticle,
    Newspaper,
    ArticleComment,
    Category,
    Company,
)
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=1)
    editors = serializers.SlugRelatedField(
        many=True, queryset=User.objects.filter(is_editor=True), slug_field="username"
    )
    owner = serializers.CharField(source="owner.username", read_only=True)
    newspapers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "editors",
            "owner",
            "newspapers",
        )
        read_only_fields = (
            "id",
            "owner",
            "newspapers",
        )

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.save()
    #     return instance


class NewsPaperSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        min_length=1, validators=[UniqueValidator(queryset=Newspaper.objects.all())]
    )
    tagline = serializers.CharField(min_length=1)
    schedule = serializers.CharField(min_length=1)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )
    articles = serializers.StringRelatedField(many=True, read_only=True)
    created_by = serializers.CharField(read_only=True, source="created_by.username")
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Newspaper
        fields = (
            "id",
            "name",
            "tagline",
            "schedule",
            "company",
            "articles",
            "created_by",
            "created_at",
        )
        read_only_fields = (
            "id",
            "articles",
            "created_by",
            "created_at",
        )


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
    editor = serializers.CharField(source="editor.username", read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)
    newspaper = serializers.SlugRelatedField(
        queryset=Newspaper.objects.all(), slug_field="name", many=True
    )

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
            "comments",
            "categories",
            "newspaper",
        )
        read_only_fields = (
            "id",
            "read_time",
            "created_at",
            "slug",
            "editor",
            "is_mainstory",
            "comments",
            "categories",
        )


class ArticleCommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    comment = serializers.CharField(min_length=1)
    commenter = serializers.CharField(source="commenter.username", read_only=True)

    class Meta:
        model = ArticleComment
        fields = (
            "id",
            "comment",
            "commenter",
            "article",
        )
        read_only_fields = (
            "id",
            "commenter",
        )


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=1)
    owner = serializers.CharField(source="owner.username", read_only=True)
    articles = serializers.SlugRelatedField(
        many=True, queryset=NewsArticle.objects.all(), slug_field="slug"
    )
    is_public = serializers.BooleanField(default=False)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "is_public",
            "owner",
            "articles",
        )
        read_only_fields = (
            "id",
            "owner",
        )
