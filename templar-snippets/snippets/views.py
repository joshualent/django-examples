from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from .models import Snippet

# Create your views here.


class SnippetListView(ListView):
    model = Snippet
    template_name = "snippets/snippet_list.html"

    def get_context_data(self, **kwargs):

        search = self.request.GET.get("search", "")
        context = super().get_context_data(
            **kwargs,
        )
        context["search"] = search
        return context

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        print()
        snippets = Snippet.objects.filter(
            title__icontains=search, _connector="OR", tags__slug__icontains=search
        )

        return snippets

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        context = response.context_data
        print(context)
        # is_htmx = self.request.GET.get("search", "") == "htmx"
        is_htmx = request.headers.get("HX-Request") == "true"
        if is_htmx:
            return render(request, "snippets/partials/_snippet_list.html", context)
        return response


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippets/snippet_detail.html"


class SnippetCreateView(CreateView):
    model = Snippet
    template_name = "snippets/snippet_new.html"
    fields = ("title", "body", "tags")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SnippetCustomCreateView(CreateView):
    model = Snippet
    template_name = "snippets/snippet_newer.html"
    fields = ("title", "body", "tags")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SnippetUpdateView(UpdateView):
    model = Snippet
    template_name = "snippets/snippet_edit.html"
    fields = ("title", "body", "tags")

class SnippetDeleteView(DeleteView):
    model = Snippet
    template_name = "snippets/snippet_delete.html"