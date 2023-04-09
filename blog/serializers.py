from blog.models import Article, ArticleBookmark, Blog, Comment, ArticleRating, Label
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        min_length=1, validators=[UniqueValidator(queryset=Blog.objects.all())]
    )
    tagline = serializers.CharField(min_length=1)
    schedule = serializers.CharField(min_length=1)
    articles = serializers.StringRelatedField(many=True, read_only=True)
    created_by = serializers.CharField(read_only=True, source="created_by.username")
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Blog
        fields = (
            "id",
            "name",
            "tagline",
            "schedule",
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


class ArticleSerializer(serializers.ModelSerializer):
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
    author = serializers.CharField(source="author.username", read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    labels = serializers.StringRelatedField(many=True, read_only=True)
    blog = serializers.SlugRelatedField(
        queryset=Blog.objects.all(), slug_field="name", many=True
    )
    rating = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "read_time",
            "created_at",
            "title",
            "subtitle",
            "image",
            "body",
            "slug",
            "author",
            "comments",
            "labels",
            "blog",
            "rating",
        )
        read_only_fields = (
            "id",
            "read_time",
            "created_at",
            "slug",
            "author",
            "comments",
            "labels",
            "rating",
        )


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    comment = serializers.CharField(min_length=1)
    commenter = serializers.CharField(source="commenter.username", read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), slug_field="title"
    )

    class Meta:
        model = Comment
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


class LabelSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=1)
    owner = serializers.CharField(source="owner.username", read_only=True)
    articles = serializers.SlugRelatedField(
        many=True, queryset=Article.objects.all(), slug_field="title"
    )
    is_public = serializers.BooleanField(default=False)

    class Meta:
        model = Label
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


class ArticleBookmarkSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    bookmarker = serializers.CharField(source="user.username", read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), slug_field="title"
    )

    class Meta:
        model = ArticleBookmark
        fields = (
            "id",
            "bookmarker",
            "article",
        )
    
    def create(self, validated_data):
        request = self.context["request"]

        validated_data["bookmarker"] = request.user
        instance, _ = ArticleBookmark.objects.get_or_create(**validated_data)

        return instance


class ArticleRatingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), slug_field="title"
    )
    rated_by = serializers.CharField(source="rated_by.username", read_only=True)
    rating = serializers.IntegerField(max_value=5, default=0)

    class Meta:
        model = ArticleRating
        fields = (
            "id",
            "article",
            "rated_by",
            "rating",
        )

    def create(self, validated_data):
        request = self.context["request"]

        validated_data["rated_by"] = request.user
        instance, _ = ArticleRating.objects.get_or_create(**validated_data)

        return instance
