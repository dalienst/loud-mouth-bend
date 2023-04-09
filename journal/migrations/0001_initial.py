# Generated by Django 4.1.7 on 2023-04-09 18:32

import ckeditor.fields
import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Journal",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "journal_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=400, null=True, unique=True
                    ),
                ),
                ("title", models.CharField(max_length=400)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="journal_images",
                    ),
                ),
                ("body", ckeditor.fields.RichTextField()),
                ("read_time", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Journal",
                "verbose_name_plural": "Journals",
                "ordering": ["-created_at", "title", "read_time"],
            },
        ),
    ]
