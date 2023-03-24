from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from news.serializers import (
    NewsArticleSerializer,
    ArticleCommentSerializer,
    CategorySerializer,
)
from news.models import NewsArticle, ArticleComment, Category
from accounts.permissions import IsEditor, MeUser
from news.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class NewsArticleListCreate(generics.ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsEditor,
    ]

    def perform_create(self, serializer):
        serializer.save(editor=self.request.user)

    def get_queryset(self):
        return NewsArticle.objects.filter(editor=self.request.user)


class AllNewsArticleList(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer


class ArticleDetail(generics.RetrieveAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


class NewsArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    lookup_field = "slug"
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsEditor,
    ]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of articles
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Article deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_queryset(self):
        return NewsArticle.objects.filter(editor=self.request.user)


class ArticleCommentListView(generics.ListCreateAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, MeUser]

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)

    def get_queryset(self):
        return ArticleComment.objects.filter(commenter=self.request.user)


class ArticleCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsUserOrReadOnly,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return ArticleComment.objects.filter(commenter=self.request.user)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, MeUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_public=True)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.filter(is_public=True)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
