from django.urls import path

from news.views import (
    NewsArticleDetail,
    NewsArticleListCreate,
    AllNewsArticleList,
    ArticleDetail,
)

urlpatterns = [
    path("articles/", NewsArticleListCreate.as_view(), name="articles-list"),
    path("articles/<int:slug>/", NewsArticleDetail.as_view(), name="articles-detail"),
    path("allarticles/", AllNewsArticleList.as_view(), name="all-articles"),
    path("article/<str:id>/", ArticleDetail.as_view(), name="article-detail"),
]
