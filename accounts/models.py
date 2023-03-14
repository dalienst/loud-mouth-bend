from django.db import models
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from accounts.abstracts import TimeStampedModel, UniversalIdModel
from datetime import date


class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, username: str, email: str, password: str, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Password is required")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, UniversalIdModel):
    """
    The Users Model
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = ["username", "password"]
    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.username


class Profile(UniversalIdModel):
    """
    Profile model
    To add more fields: website, location and contact
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(blank=True, max_length=500, null=True)
    lastname = models.CharField(blank=True, max_length=500, null=True)
    image = CloudinaryField(
        "images",
    )
    bio = models.CharField(blank=True, max_length=500, null=True)

    def __str__(self) -> str:
        return self.user
