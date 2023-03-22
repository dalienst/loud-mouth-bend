from django.contrib import admin
from news.models import NewsArticle, Newspaper, Category, ArticleComment

admin.site.register(Newspaper)
admin.site.register(Category)
admin.site.register(NewsArticle)
admin.site.register(ArticleComment)
