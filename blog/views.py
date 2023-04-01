from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from blog.models import Article, ArticleBookmark, Blog, Comment, ArticleRating, Label
from blog.serializers import (
    ArticleSerializer,
    ArticleRatingSerializer,
    ArticleBookmarkSerializer,
    CommentSerializer,
    BlogSerializer,
    LabelSerializer,
)
from accounts.permissions import IsUser
from news.permissions import IsUserOrReadOnly
from blog.permissions import IsOwnerOrReadOnly


class BlogListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsUser,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Blog.objects.filter(created_by=self.request.user)


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsUser,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return Blog.objects.filter(created_by=self.request.user)


class AllBlogsListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class AllBlogsDetailView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "id"


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class AllArticlesListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class AllArticlesDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "id"


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(commenter=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        return Comment.objects.filter(commenter=self.request.user)


class LabelListCreateView(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)


class LabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"


class LabelListView(generics.ListAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Label.objects.filter(is_public=True)


class BookmarkListCreateView(generics.ListCreateAPIView):
    queryset = ArticleBookmark.objects.all()
    serializer_class = ArticleBookmarkSerializer
    permission_classes = [IsUser, IsAuthenticated]

    def get_queryset(self):
        return ArticleBookmark.objects.filter(user=self.request.user)


class BookmarkDetailView(generics.ListCreateAPIView):
    queryset = ArticleBookmark.objects.all()
    serializer_class = ArticleBookmarkSerializer
    permission_classes = [IsUser, IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return ArticleBookmark.objects.filter(user=self.request.user)


class RatingListCreateView(generics.ListCreateAPIView):
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ArticleRating.objects.filter(rated_by=self.request.user)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleRatingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return ArticleRating.objects.filter(rated_by=self.request.user)
