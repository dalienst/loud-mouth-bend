from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from accounts.models import Profile
from accounts.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)
from news.models import Company
from blog.serializers import ArticleBookmarkSerializer, ArticleRatingSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of the user model
    User is able to create an account
    An instance of Profile is created once the user registers
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )
    story = serializers.StringRelatedField(many=True, read_only=True)
    comment = serializers.StringRelatedField(many=True, read_only=True)
    bookmark = ArticleBookmarkSerializer(many=True, read_only=True)
    rated = ArticleRatingSerializer(many=True, read_only=True)
    commenter = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "is_verified",
            "is_editor",
            "is_admin",
            "story",
            "comment",
            "bookmark",
            "rated",
            "commenter",
            "category",
        )
        read_only_fields = (
            "id",
            "is_verified",
            "is_editor",
            "is_admin",
            "story",
            "comment",
            "bookmark",
            "rated",
            "commenter",
            "category",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        Profile.objects.create(user=user)
        return user


class AdminSerializer(serializers.ModelSerializer):
    """
    Create admin creation endpoints
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )
    articles = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)
    newspaper = serializers.StringRelatedField(many=True, read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "is_verified",
            "is_editor",
            "is_admin",
            "articles",
            "category",
            "company",
            "newspaper",
        )
        read_only_fields = (
            "id",
            "is_verified",
            "is_editor",
            "is_admin",
            "articles",
            "category",
            "company",
            "newspaper",
        )

    def create(self, validated_data):
        admin = User.objects.create_user(**validated_data)
        admin.is_editor = True
        admin.is_admin = True
        admin.is_verified = True
        admin.is_staff = True
        admin.save()
        Profile.objects.create(user=admin)
        Company.objects.create(owner=admin)
        return admin


class EditorSerializer(serializers.ModelSerializer):
    """
    Create editor creation endpoints
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )
    articles = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)
    companies = serializers.StringRelatedField(many=True, read_only=True)
    newspaper = serializers.StringRelatedField(many=True, read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "is_verified",
            "is_editor",
            "is_admin",
            "articles",
            "category",
            "companies",
            "newspaper",
            "company",
        )
        read_only_fields = (
            "id",
            "is_verified",
            "is_editor",
            "is_admin",
            "articles",
            "category",
            "companies",
            "newspaper",
            "company",
        )

    def create(self, validated_data):
        editor = User.objects.create_user(**validated_data)
        editor.is_editor = True
        editor.is_verified = True
        editor.save()
        Profile.objects.create(user=editor)
        return editor


class ProfileSerializer(serializers.ModelSerializer):
    """
    The profile serializer to enable retrieval and updating of profile of the user
    """

    username = serializers.CharField(read_only=True, source="user.username")
    image = serializers.ImageField(use_url=True, required=False)
    firstname = serializers.CharField(allow_blank=True, required=False)
    lastname = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ("username", "bio", "image", "firstname", "lastname")

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.image = validated_data.get("image", instance.image)
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type:ignore[no-untyped-def]
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):  # type:ignore[no-untyped-def]
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError(
                "Invalid or expired token", code="invalid_token"
            )
