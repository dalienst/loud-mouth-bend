from django.contrib import admin
from news.models import NewsArticle, Newspaper

admin.site.register(Newspaper)
# admin.site.register(Category)
admin.site.register(NewsArticle)
