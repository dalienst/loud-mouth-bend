"""
Journals application. 
A user can keep journals of their daily life.
The journals can only be read by the user or rather the person who
wrote them.
In a later update, a feature to enable the user make the journals
public will be added.
"""

from django.db import models
from django.contrib.auth import get_user_model
from accounts.abstracts import TimeStampedModel
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import uuid
import math

User = get_user_model()


class Journal(TimeStampedModel):
    """
    Model to store the journals.
    These are meant to be private and only be seen by the author
    Author in this case user
    TODO: Add a boolean field to allow user make journals private
    Also, checkout the date issue
    """

    journal_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    title = models.CharField(max_length=400, blank=False, null=False)
    image = CloudinaryField("journal_images", blank=True, null=True)
    body = RichTextField()
    read_time = models.PositiveIntegerField(blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="author", null=True
    )

    class Meta:
        ordering = ["-created_at", "title", "read_time"]
        verbose_name = "Journal"
        verbose_name_plural = "Journals"

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Journal)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.title}-{instance.journal_id}")


@receiver(pre_save, sender=Journal)
def reading_time_pre_save(sender, instance, **kwargs) -> None:
    instance.read_time = math.ceil(instance.body.count(" ") // 200)
