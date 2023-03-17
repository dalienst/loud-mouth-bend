from django.contrib import admin
from news.models import NewsArticle, Newspaper, NewsArticleCategory

admin.site.register(Newspaper)
admin.site.register(NewsArticleCategory)
admin.site.register(NewsArticle)
