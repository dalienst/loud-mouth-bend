from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from journal.models import Journal
from journal.serializers import JournalSerializer
from journal.permissions import IsOwnerOrReadOnly


class JournalListCreateView(generics.ListCreateAPIView):
    """
    create a journal
    TODO: add filters
    """

    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [IsOwnerOrReadOnly,]

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class JournalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, read or delete a journal
    """

    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "slug"

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of journals
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Journal deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
