from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from django.views import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse

from .models import Article
from .forms import CommentForm

# Create your views here.


class ArticleListView(ListView):
    """Article List View"""

    permission_required = [""]

    model = Article
    template_name = "article_list.html"


class ArticleDetailView(DetailView, FormView):
    """Article Detail View"""

    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        self.article = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """What to do when form is valid"""
        comment = form.save(commit=False)
        comment.article = self.article
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Where to go on success"""
        return reverse("article_detail", kwargs={"pk": self.article.pk})

    def get_context_data(self, **kwargs):
        """Get any additional template context"""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


# class CommentGet(DetailView):
#     """Comment GET view"""

#     model = Article
#     template_name = "article_detail.html"

#     def get_context_data(self, **kwargs):
#         """Get any additional template context"""
#         context = super().get_context_data(**kwargs)
#         context["form"] = CommentForm()
#         return context


# class CommentPost(SingleObjectMixin, FormView):
#     """Comment POST view"""

#     model = Article
#     form_class = CommentForm
#     template_name = "article_detail.html"

#     def post(self, request, *args, **kwargs):
#         """Handle POST request"""
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         """What to do when form is valid"""
#         comment = form.save(commit=False)
#         comment.article = self.object
#         comment.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         """Where to go on success"""
#         article = self.object
#         return reverse("article_detail", kwargs={"pk": article.pk})


# class ArticleDetailView(LoginRequiredMixin, View):
#     """Article Detail View"""

#     def get(self, request, *args, **kwargs):
#         """Handle GET request"""
#         view = CommentGet.as_view()
#         return view(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         """Handle POST request"""
#         view = CommentPost.as_view()
#         return view(request, *args, **kwargs)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Article Create View"""

    model = Article
    template_name = "article_create.html"
    fields = ("title", "body")

    def form_valid(self, form):
        """Add author to form on save"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Article created successfully!"
        )
        return super().get_success_url()


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Article Update View"""

    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):
        """Test func for UserPassesTestMixin"""
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Article updated successfully!"
        )
        return super().get_success_url()


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Article Delete View"""

    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        """Test func for UserPassesTestMixin"""
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        # send messages using django's message app
        messages.add_message(
            self.request, messages.SUCCESS, "Article deleted successfully!"
        )
        return super().get_success_url()


class ArticleLikeView(LoginRequiredMixin, View):
    """Article Like View"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        # request.GET holds the query params, access with a string name
        # and a default value if not found
        article_id = request.GET.get("article_id", None)
        article_action = request.GET.get("article_action", None)

        if not article_id or not article_action:
            return JsonResponse(
                {
                    "success": False,
                }
            )
        article = Article.objects.get(id=article_id)
        like_count = article.likes.count()
        user_liked = request.user in article.likes.all()
        if article_action == "like":
            article.likes.add(request.user)
            actual_action = "like"
        else:
            article.likes.remove(request.user)
            actual_action = "unlike"
        return JsonResponse(
            {
                "success": True,
                "action": actual_action,
                "like_count": like_count,
            }
        )
