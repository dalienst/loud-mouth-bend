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

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "is_verified")
        read_only_fields = ("id", "is_verified")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        Profile.objects.create(user=user)
        return user


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
        fields = (
            "username",
            "bio",
            "image",
            "firstname",
            "lastname"
        )

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
