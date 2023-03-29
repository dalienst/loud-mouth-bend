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
    CategoryDetailView,
    CompanyListCreateView,
    CompanyDetailView,
    CompanyListView,
    CompanyDetail,
    NewspaperListCreateView,
    NewspaperDetailView,
    NewspaperListView,
    NewspaperDetail,
)

urlpatterns = [
    path("company/", CompanyListCreateView.as_view(), name="company-list"),
    path("company/<str:id>/", CompanyDetailView.as_view(), name="company-detail"),
    path("companies/", CompanyListView.as_view(), name="all-companies"),
    path("companies<str:id>/", CompanyDetail.as_view(), name="companies-detail"),
    path("newspaper/", NewspaperListCreateView.as_view(), name="newspaper-list"),
    path("newspaper/<str:id>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/", NewspaperListView.as_view(), name="newspapers-list"),
    path("newspapers/<str:id>/", NewspaperDetail.as_view(), name="newspapers-detail"),
    path("articles/", NewsArticleListCreate.as_view(), name="articles-list"),
    path("articles/<str:slug>/", NewsArticleDetail.as_view(), name="articles-detail"),
    path("allarticles/", AllNewsArticleList.as_view(), name="all-articles"),
    path("article/<str:id>/", ArticleDetail.as_view(), name="article-detail"),
    path(
        "comment/",
        ArticleCommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "comment/<str:id>/",
        ArticleCommentDetailView.as_view(),
        name="comment-detail",
    ),
    path("category/", CategoryListCreateView.as_view(), name="category-list"),
    path("category/<str:id>/", CategoryDetail.as_view(), name="category-detail"),
    path("categories/", CategoryListView.as_view(), name="categories-list"),
    path(
        "categories/<str:id>/", CategoryDetailView.as_view(), name="categories-detail"
    ),
]
