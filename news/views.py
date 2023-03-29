from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from news.serializers import (
    NewsArticleSerializer,
    ArticleCommentSerializer,
    CategorySerializer,
    NewsPaperSerializer,
    CompanySerializer,
)
from news.models import NewsArticle, ArticleComment, Category, Newspaper, Company
from accounts.permissions import IsEditor, MeUser, IsAdmin
from news.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdmin,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Company.objects.filter(created_by=self.request.user)


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdmin,
    ]
    lookup_field = "id"

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of companies
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Company deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_queryset(self):
        return Company.objects.filter(created_by=self.request.user)


class CompanyDetail(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "id"


class NewspaperListCreateView(generics.ListCreateAPIView):
    queryset = Newspaper.objects.all()
    serializer_class = NewsPaperSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdmin,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Newspaper.objects.filter(created_by=self.request.user)


class NewspaperListView(generics.ListAPIView):
    queryset = Newspaper.objects.all()
    serializer_class = NewsPaperSerializer


class NewspaperDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newspaper.objects.all()
    serializer_class = NewsPaperSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdmin,
    ]
    lookup_field = "id"

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of companies
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Company deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_queryset(self):
        return Newspaper.objects.filter(created_by=self.request.user)


class NewspaperDetail(generics.RetrieveAPIView):
    queryset = Newspaper.objects.all()
    serializer_class = NewsPaperSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "id"


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
