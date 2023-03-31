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
    CompanyDetailView,
    AdminCompanyListView,
    CompanyDetail,
    NewspaperListCreateView,
    NewspaperDetailView,
    NewspaperListView,
    NewspaperDetail,
    CompanyListView,
    ArticleCompanyList,
    NewsInstanceListCreateView,
    NewsInstanceDetailView,
    NewsTodayWeeklyMonthyListView,
    NewsTodayWeeklyMonthyDetailView,
)

urlpatterns = [
    # Company urls
    path("company/", AdminCompanyListView.as_view(), name="company-list"),
    path("company/<str:owner>/", CompanyDetailView.as_view(), name="company-detail"),
    path("companies/", CompanyListView.as_view(), name="all-companies"),
    path("companies<str:id>/", CompanyDetail.as_view(), name="companies-detail"),
    # Newspapers urls
    path("newspaper/", NewspaperListCreateView.as_view(), name="newspaper-list"),
    path("newspaper/<str:id>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/", NewspaperListView.as_view(), name="newspapers-list"),
    path("newspapers/<str:id>/", NewspaperDetail.as_view(), name="newspapers-detail"),
    # Articles urls
    path("articles/", NewsArticleListCreate.as_view(), name="articles-list"),
    path("articles/<str:slug>/", NewsArticleDetail.as_view(), name="articles-detail"),
    path("allarticles/", AllNewsArticleList.as_view(), name="all-articles"),
    path("artcompany/", ArticleCompanyList.as_view(), name="company-articles"),
    path("article/<str:id>/", ArticleDetail.as_view(), name="article-detail"),
    # News Instances urls
    path("paper/", NewsInstanceListCreateView.as_view(), name="paper-list"),
    path("paper/<str:id>/", NewsInstanceDetailView.as_view(), name="paper-detail"),
    path("papers/", NewsTodayWeeklyMonthyListView.as_view(), name="papers-list"),
    path(
        "papers/<str:id>/",
        NewsTodayWeeklyMonthyDetailView.as_view(),
        name="papers-detail",
    ),
    # Comment urls
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
    # Category urls
    path("category/", CategoryListCreateView.as_view(), name="category-list"),
    path("category/<str:id>/", CategoryDetail.as_view(), name="category-detail"),
    path("categories/", CategoryListView.as_view(), name="categories-list"),
    path(
        "categories/<str:id>/", CategoryDetailView.as_view(), name="categories-detail"
    ),
]
