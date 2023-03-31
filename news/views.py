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
    NewsInstanceSerializer,
)
from news.models import (
    NewsArticle,
    ArticleComment,
    Category,
    Newspaper,
    Company,
    NewsInstance,
)
from accounts.permissions import IsEditor, MeUser, IsAdmin, IsAdminOrReadOnly
from news.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class AdminCompanyListView(generics.ListAPIView):
    """
    Admins/chief editors see the company created for them
    as soon as they create an account on the site.
    One company for every admin.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdmin,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin updates their company.
    The company is created when they create an account.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdmin,
    ]
    lookup_field = "owner"

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
        return Company.objects.filter(owner=self.request.user)


class CompanyListView(generics.ListAPIView):
    """
    Users see the companies created
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class CompanyDetail(generics.RetrieveAPIView):
    """
    Users see the details of the company
    """

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
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class NewspaperDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newspaper.objects.all()
    serializer_class = NewsPaperSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    lookup_field = "id"

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of companies
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Newspaper deleted successfully"},
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
    """
    Editor creates an article.
    The editor has to write for a newspaper.
    TODO: Restrict creations of articles to only editors included
    in a specific company.
    """

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
    """
    Enables users see the news articles.
    They do not need to be authenticated.
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer


class ArticleDetail(generics.RetrieveAPIView):
    """
    User sees the details of the article
    User needs to be authenticated.
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


class NewsArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Editor of the article updates the article.
    Only the editor is allowed to edit their article.
    Permission yet to be given to the admin.
    """

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


class ArticleCompanyList(generics.ListAPIView):
    """
    This view allows owner of the company see the articles
    of the company.
    Allows the chief editor create the News Instances of the day.
    """

    serializer_class = NewsArticleSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]

    def get_queryset(self):
        return NewsArticle.objects.filter(newspaper__company__owner=self.request.user)


class NewsInstanceListCreateView(generics.ListCreateAPIView):
    """
    An instance of the newspaper is created by the chief editor and
    released to the user. The instance is based on the status of the
    magazine/newspaper.
    """

    serializer_class = NewsInstanceSerializer
    queryset = NewsInstance.objects.all()
    permission_classes = [
        IsAdmin,
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return NewsInstance.objects.filter(created_by=self.request.user)


class NewsInstanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Chief editor updates the instance
    TODO: add feature of self destroy: check django cellery
    """

    serializer_class = NewsInstanceSerializer
    queryset = NewsInstance.objects.all()
    permission_classes = [
        IsAdminOrReadOnly,
        IsAuthenticated,
    ]
    lookup_field = "id"

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of companies
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Newspaper deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_queryset(self):
        return NewsInstance.objects.filter(created_by=self.request.user)


class NewsTodayWeeklyMonthyListView(generics.ListAPIView):
    """
    readers see the list of news released on that month, day or week
    """

    serializer_class = NewsInstanceSerializer
    queryset = NewsInstance.objects.all()


class NewsTodayWeeklyMonthyDetailView(generics.RetrieveAPIView):
    """
    Readers get the details of the news
    """

    serializer_class = NewsInstanceSerializer
    queryset = NewsInstance.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "id"


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
