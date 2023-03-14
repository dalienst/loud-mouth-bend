from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from journal.models import Journal

User = get_user_model()


class JournalSerializer(serializers.ModelSerializer):
    journal_id = serializers.CharField(
        read_only=True,
    )
    read_time = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(
        max_length=400,
        min_length=20,
    )
    image = serializers.ImageField(use_url=True, required=False)
    body = serializers.CharField(
        min_length=20,
    )
    slug = serializers.SlugField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Journal
        fields = (
            "journal_id",
            "slug",
            "title",
            "read_time",
            "image",
            "body",
            "author",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "journal_id",
            "created_at",
            "updated_at",
            "read_time",
            "author",
        )

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["author"] = request.user
        instance = Journal.objects.create(**validated_data)
        return instance
