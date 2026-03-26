from django.urls import path

from .views import (
    CroakListView,
    CroakDetailView,
    CroakUpdateView,
    CroakCreateView,
    CroakDeleteView,
    CroakLikeView,
    # CroakLikeHtmxView,
)

urlpatterns = [
    path("new/", CroakCreateView.as_view(), name="croak_new"),
    path("<int:pk>/edit/", CroakUpdateView.as_view(), name="croak_edit"),
    path("<int:pk>/confirm-delete", CroakDeleteView.as_view(), name="croak_delete"),
    path("<int:pk>/", CroakDetailView.as_view(), name="croak_detail"),
    path("<int:pk>/like", CroakLikeView.as_view(), name="croak_like"),
    # path(
    #     "htmx/<int:croak_pk>/like/", CroakLikeHtmxView.as_view(), name="croak_like_htmx"
    # ),
    path("", CroakListView.as_view(), name="home"),
]
