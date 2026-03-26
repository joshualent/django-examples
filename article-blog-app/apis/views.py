from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.urls import reverse

from articles.models import Article, Comment


# Create your views here.
class ApiCommentDetailView(LoginRequiredMixin, View):
    """Comment detail view"""

    def get(self, request, article_pk, comment_pk, *args, **kwargs):
        """GET request"""
        comment = Comment.objects.values().get(pk=comment_pk)
        return JsonResponse(comment, safe=False)


class ApiCommentListView(LoginRequiredMixin, View):
    """Comment list view"""

    def get(self, request, article_pk, *args, **kwargs):
        comments = list(
            Comment.objects.filter(article_id=article_pk).values(),
        )
        for comment in comments:
            reversed_url = reverse(
                "api_comment_detail",
                kwargs={
                    "article_pk": comment["article_id"],
                    "comment_pk": comment["id"],
                },
            )
            comment["detail_url"] = request.build_absolute_uri(
                reversed_url,
            )
        return JsonResponse(comments, safe=False)


class ApiArticleDetailView(LoginRequiredMixin, View):
    """Article Detail View"""

    def get(self, request, article_pk, *args, **kwargs):
        """GET request"""
        article = Article.objects.values().get(pk=article_pk)
        comments = list(
            Comment.objects.filter(article_id=article_pk).values(),
        )
        reversed_url = reverse(
            "api_comment_list",
            kwargs={"article_pk": article["id"]},
        )
        article["comment_list_url"] = request.build_absolute_uri(reversed_url)
        article["comments"] = comments
        return JsonResponse(article, safe=False)


class ApiArticleListView(LoginRequiredMixin, View):
    """Api Article list view"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        articles = list(Article.objects.values())
        for article in articles:
            article["detail_url"] = request.build_absolute_uri(
                reverse("api_article_detail", kwargs={"article_pk": article["id"]})
            )
        return JsonResponse(articles, safe=False)
