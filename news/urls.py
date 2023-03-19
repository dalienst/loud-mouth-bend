from django.urls import path

from news.views import (
    NewsArticleDetail,
    NewsArticleListCreate,
    AllNewsArticleList,
    ArticleDetail,
    ArticleCommentListView,
    ArticleCommentDetailView,
)

urlpatterns = [
    path("articles/", NewsArticleListCreate.as_view(), name="articles-list"),
    path("articles/<int:slug>/", NewsArticleDetail.as_view(), name="articles-detail"),
    path("allarticles/", AllNewsArticleList.as_view(), name="all-articles"),
    path("article/<str:id>/", ArticleDetail.as_view(), name="article-detail"),
    path(
        "comment/",
        ArticleCommentListView.as_view(),
        name="articlecomment-list",
    ),
    path(
        "comment/<str:id>/",
        ArticleCommentDetailView.as_view(),
        name="articlecomment-detail",
    ),
]
