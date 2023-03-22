from django.urls import path

from news.views import (
    NewsArticleDetail,
    NewsArticleListCreate,
    AllNewsArticleList,
    ArticleDetail,
    ArticleCommentListView,
    ArticleCommentDetailView,
    CategoryDetail,
    CategoryListCreateView,
    CategoryListView,
    NewsCategoryListView,
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
    path("category/", CategoryListCreateView.as_view(), name="category-list"),
    path("category/<str:id>/", CategoryDetail.as_view(), name="category-detail"),
    path("categories/", CategoryListView.as_view(), name="categories-list"),
    path("newscategories/", NewsCategoryListView.as_view(), name="newscategories-list"),
]
