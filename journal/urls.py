from django.urls import path
from journal.views import JournalListCreateView, JournalDetailView

urlpatterns = [
    path("journal/", JournalListCreateView.as_view(), name="journal-list"),
    path("journal/<slug:slug>/", JournalDetailView.as_view(), name="journal-detail"),
]
