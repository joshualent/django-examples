from django.urls import path

from .views import (
    SnippetListView,
    SnippetDetailView,
    SnippetCustomCreateView,
    SnippetCreateView,
    SnippetUpdateView,
    SnippetDeleteView
)


urlpatterns = [
    path("", SnippetListView.as_view(), name="snippet_list"),
    path("<int:pk>/", SnippetDetailView.as_view(), name="snippet_detail"),
    path("new/", SnippetCreateView.as_view(), name="snippet_new"),
    path("newer/", SnippetCustomCreateView.as_view(), name="snippet_newer"),
    path("<int:pk>/edit", SnippetUpdateView.as_view(), name="snippet_edit"),
    path("<int:pk>/confirm-delete", SnippetDeleteView.as_view(), name="snippet_delete"),
]
