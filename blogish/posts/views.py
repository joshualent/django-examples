from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import View, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.


class PostListView(ListView):
    """Post List View"""

    template_name = "posts/post_list.html"
    model = Post


class PostDetailView(DetailView, FormView):
    """Post List View"""

    template_name = "posts/post_detail.html"
    model = Post
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        self.post = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Complete form information after validation succeeds"""
        comment = form.save(commit=False)
        comment.post = self.post
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Success redirect URL"""
        return reverse("post_detail", kwargs={"pk": self.post.pk})


class PostCreateView(LoginRequiredMixin, CreateView):
    """Post Create View"""

    model = Post
    template_name = "posts/post_new.html"
    fields = ("title", "body", "public")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Post Update View"""

    model = Post
    template_name = "posts/post_edit.html"
    fields = ("title", "body", "public")


class PostLikeView(View):
    """Post Like endpoint for HTMX"""

    def post(self, request, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user.id)
            post.save()
        else:
            post.likes.add(request.user.id)
            post.save()

        return render(request, "posts/partials/_post_like.html", {"post": post})


class CommentLikeView(View):
    """Post Like endpoint for HTMX"""

    def post(self, request, comment_pk, *args, **kwargs):
        comment = Comment.objects.get(pk=comment_pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user.id)
            comment.save()
        else:
            comment.likes.add(request.user.id)
            comment.save()

        return render(
            request, "posts/partials/_comment_like.html", {"comment": comment}
        )


class CommentUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        return render(
            request, "posts/partials/_comment_edit.html", {"comment": comment}
        )

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user:
            return HttpResponseForbidden("You are not allowed to edit this comment.")
        comment.text = request.POST.get("text")
        comment.save()
        return render(
            request,
            "posts/partials/_comment.html",
            {"comment": comment},
        )


class CommentDetailView(DetailView):
    model = Comment
    template_name = "posts/partials/_comment_edit.html"
