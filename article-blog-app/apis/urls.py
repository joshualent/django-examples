from django.urls import path

from .views import (
    ApiCommentListView,
    ApiCommentDetailView,
    ApiArticleDetailView,
    ApiArticleListView,
)

urlpatterns = [
    path(
        "articles/<int:article_pk>/comments/<int:comment_pk>/",
        ApiCommentDetailView.as_view(),
        name="api_comment_detail",
    ),
    path(
        "articles/<int:article_pk>/comments/",
        ApiCommentListView.as_view(),
        name="api_comment_list",
    ),
    path(
        "articles/<int:article_pk>/",
        ApiArticleDetailView.as_view(),
        name="api_article_detail",
    ),
    path(
        "articles/",
        ApiArticleListView.as_view(),
        name="api_article_list",
    ),
]
