from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from news.serializers import NewsArticleSerializer
from news.models import NewsArticle
from accounts.permissions import IsEditor


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
