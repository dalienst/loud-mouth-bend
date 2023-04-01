from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import math


from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


from accounts.abstracts import UniversalIdModel, TimeStampedModel

User = get_user_model()


class Blog(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=400, blank=False, null=False)
    tagline = models.CharField(max_length=400, blank=False, null=False)

    BLOG_SCHEDULE = (
        ("D", "Daily"),
        ("W", "Weekly"),
        ("M", "Monthly"),
        ("Y", "Yearly"),
    )
    schedule = models.CharField(max_length=1, choices=BLOG_SCHEDULE, default="D")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog")

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"


class Article(UniversalIdModel, TimeStampedModel):
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    title = models.CharField(max_length=400, blank=False, null=False)
    subtitle = models.CharField(max_length=1000, blank=True, null=True)
    image = CloudinaryField("blog_images", blank=True, null=True)
    body = RichTextField()
    read_time = models.PositiveIntegerField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="story")
    blog = models.ManyToManyField(Blog, related_name="articles", blank=False)
    # TODO: look into tags

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Article)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.title}-{instance.id}")


@receiver(pre_save, sender=Article)
def reading_time_pre_save(sender, instance, **kwargs) -> None:
    instance.read_time = math.ceil(instance.body.count(" ") // 200)


class Comment(TimeStampedModel, UniversalIdModel):
    commenter = models.ForeignKey(
        User, related_name="comment", on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE
    )
    comment = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self) -> str:
        return self.comment


class Label(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=400, blank=False, null=False, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="label")
    is_public = models.BooleanField(default=False)
    articles = models.ManyToManyField(Article, related_name="labels")

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = "Labels"

    def __str__(self) -> str:
        return self.name


class ArticleBookmark(TimeStampedModel, UniversalIdModel):
    """
    Bookmark model to store the articles bookmarked by a reader
    """

    bookmarker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmark")
    # TODO: figure out if its M2M or O2M
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="bookmarks"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"



class ArticleRating(TimeStampedModel, UniversalIdModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="rating"
    )
    rated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rated"
    )
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self) -> str:
        return f"{self.rating} stars"
