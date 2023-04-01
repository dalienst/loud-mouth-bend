from django.urls import path

from blog.views import (
    BlogListCreateView,
    BlogDetailView,
    AllBlogsDetailView,
    AllBlogsListView,
    ArticleDetailView,
    AllArticlesDetailView,
    ArticleListCreateView,
    AllArticlesListView,
    LabelListCreateView,
    LabelListView,
    RatingListCreateView,
    CommentListCreateView,
    BookmarkListCreateView,
    LabelDetailView,
    RatingDetailView,
    CommentDetailView,
    BookmarkDetailView,
)

urlpatterns = [
    # Blogs
    path("blog", BlogListCreateView.as_view(), name="blog-list"),
    path("blog/<str:id>/", BlogDetailView.as_view(), name="blog-detail"),
    path("blogs", AllBlogsListView.as_view(), name="blogs-list"),
    path("blogs/<str:id>/", AllBlogsDetailView.as_view(), name="blog-create"),
    # Stories
    path("story/", ArticleListCreateView.as_view(), name="story-list"),
    path("story/<str:id>/", ArticleDetailView.as_view(), name="story-detail"),
    path("stories/", AllArticlesListView.as_view(), name="stories-list"),
    path("stories/<str:id>/", AllArticlesDetailView.as_view(), name="stories-detail"),
    # Comments
    path("comment/", CommentListCreateView.as_view(), name="artcomment-detail"),
    path("comment/<str:id>/", CommentDetailView.as_view(), name="artcomment-detail"),
    # Labels
    path("label/", LabelListCreateView.as_view(), name="label-list"),
    path("label/<str:id>/", LabelDetailView.as_view(), name="label-detail"),
    path("labels/", LabelListView.as_view(), name="labels-list"),
    # Ratings
    path("rate/", RatingListCreateView.as_view(), name="rate-list"),
    path("rate/<str:id>/", RatingDetailView.as_view(), name="rate-detail"),
    # Bookmark
    path("bookmark/", BookmarkListCreateView.as_view(), name="bookmark-list"),
    path("bookmark/<str:id>/", BookmarkDetailView.as_view(), name="bookmark-detail"),
]
