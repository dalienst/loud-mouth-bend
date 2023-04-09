from django.contrib import admin
from blog.models import Article, ArticleBookmark, Blog, Comment, ArticleRating, Label

admin.site.register(Blog)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Label)
admin.site.register(ArticleRating)
admin.site.register(ArticleBookmark)
