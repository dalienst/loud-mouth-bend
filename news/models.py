from django.db import models
from accounts.abstracts import UniversalIdModel, TimeStampedModel
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import math

User = get_user_model()


class Company(UniversalIdModel, TimeStampedModel):
    """
    The newspaper company
    A company can have very many newspapers
    A company can have very many editors
    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=400, blank=False, null=False, default="")
    editors = models.ManyToManyField(User, related_name="companies")
    # newspapers = models.ManyToManyField(Newspaper, related_name="newspapers")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.name


class Newspaper(UniversalIdModel, TimeStampedModel):
    """
    A newspaper company could have different types of
    newspapers.
    The admin creates the newspaper.
    """

    name = models.CharField(max_length=400, blank=False, null=False)
    tagline = models.CharField(max_length=400, blank=False, null=False)

    PAPER_SCHEDULE = (
        ("D", "Daily"),
        ("W", "Weekly"),
        ("M", "Monthly"),
        ("Y", "Yearly"),
    )
    schedule = models.CharField(max_length=1, choices=PAPER_SCHEDULE, default="D")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="newspapers"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="newspaper"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newspaper"
        verbose_name_plural = "Newspapers"

    def __str__(self) -> str:
        return self.name


class NewsArticle(UniversalIdModel, TimeStampedModel):
    """
    News Articles
    A boolean flag to determine which article is displayed on main page
    """

    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    title = models.CharField(max_length=400, blank=False, null=False)
    subtitle = models.CharField(max_length=1000, blank=True, null=True)
    image = CloudinaryField("news_images", blank=True, null=True)
    body = RichTextField()
    read_time = models.PositiveIntegerField(blank=True, null=True)
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    is_mainstory = models.BooleanField(default=False)
    newspaper = models.ManyToManyField(Newspaper, related_name="articles", blank=False)

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=NewsArticle)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.title}-{instance.id}")


@receiver(pre_save, sender=NewsArticle)
def reading_time_pre_save(sender, instance, **kwargs) -> None:
    instance.read_time = math.ceil(instance.body.count(" ") // 200)


class NewsInstance(UniversalIdModel):
    day = models.DateField()
    newspaper = models.ForeignKey(
        Newspaper, related_name="newspaper_instance", on_delete=models.CASCADE
    )
    articles = models.ManyToManyField(NewsArticle, related_name="news_of_the_day")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-day"]
        verbose_name = "News Instance"
        verbose_name_plural = "News Instances"

    def __str__(self) -> str:
        return f"{self.day} - {self.newspaper.name}"


class ArticleComment(UniversalIdModel, TimeStampedModel):
    """
    Comments for the news article
    """

    commenter = models.ForeignKey(
        User, related_name="commenter", on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        NewsArticle, related_name="comments", on_delete=models.CASCADE
    )
    comment = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "News Article Comment"
        verbose_name_plural = "News Article Comments"

    def __str__(self) -> str:
        return self.comment


class Category(TimeStampedModel, UniversalIdModel):
    name = models.CharField(max_length=400, blank=False, null=False, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category")
    is_public = models.BooleanField(default=False)
    articles = models.ManyToManyField(NewsArticle, related_name="categories")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
