from django.contrib import admin
from news.models import (
    NewsArticle,
    Newspaper,
    Category,
    ArticleComment,
    Company,
    NewsInstance,
)

admin.site.register(Company)
admin.site.register(Newspaper)
admin.site.register(Category)
admin.site.register(NewsArticle)
admin.site.register(NewsInstance)
admin.site.register(ArticleComment)
