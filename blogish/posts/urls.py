from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostLikeView,
    CommentLikeView,
    CommentUpdateView,
    CommentDetailView,
)


urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/edit", PostUpdateView.as_view(), name="post_edit"),
    path(
        "comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "comments/<int:pk>/edit",
        CommentUpdateView.as_view(),
        name="comment_edit",
    ),
    path("posts/post/<int:post_pk>/like", PostLikeView.as_view(), name="post_like"),
    path(
        "posts/comment/<int:comment_pk>/like",
        CommentLikeView.as_view(),
        name="comment_like",
    ),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("posts/new", PostCreateView.as_view(), name="post_new"),
]
