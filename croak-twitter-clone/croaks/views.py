from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Croak
from .forms import CommentForm

# Create your views here.


class CroakListView(ListView):
    """Croak List View"""

    model = Croak
    template_name = "croak_list.html"


class CroakDetailView(LoginRequiredMixin, DetailView, FormView):
    """Croak Detail View"""

    model = Croak
    form_class = CommentForm
    template_name = "croak_detail.html"

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        self.croak = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """What to od when form is valid"""
        comment = form.save(commit=False)
        comment.croak = self.croak
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Where to go on success"""
        return reverse("croak_detail", kwargs={"pk": self.croak.pk})

    def get_context_data(self, **kwargs):
        """Get any additional template context"""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CroakUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Croak Update View"""

    model = Croak
    template_name = "croak_edit.html"
    fields = ("body", "image_url")

    def test_func(self):
        """UserPassesTestMixin test function"""
        obj = self.get_object()
        return obj.author == self.request.user


class CroakCreateView(LoginRequiredMixin, CreateView):
    """Croak Create View"""

    model = Croak
    template_name = "croak_new.html"
    fields = ("body", "image_url")

    def form_valid(self, form):
        """Validate form on save"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class CroakDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Croak Delete View"""

    model = Croak
    template_name = "croak_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        """UserPassesTestMixin test function"""
        obj = self.get_object()
        return obj.author == self.request.user


class CroakLikeView(LoginRequiredMixin, View):
    """Croak Like View using AJAX"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        # request.GET holds the query params, access with a string name
        # and a default value if not found
        croak_id = request.GET.get("croak_id", None)
        croak_action = request.GET.get("croak_action", None)

        if not croak_id or not croak_action:
            return JsonResponse(
                {
                    "success": False,
                }
            )
        croak = Croak.objects.get(id=croak_id)
        if croak_action == "like":
            croak.likes.add(request.user)
            actual_action = "like"
        else:
            croak.likes.remove(request.user)
            actual_action = "unlike"

        like_count = croak.likes.count()
        return JsonResponse(
            {
                "success": True,
                "action": actual_action,
                "like_count": like_count,
            }
        )


# class CroakLikeHtmxView(View):
#     """Croak Like endpoint for HTMX"""

#     def post(self, request, croak_pk, *args, **kwargs):
#         croak = Croak.objects.get(pk=croak_pk)
#         liked = True
#         if request.user in croak.likes.all():
#             croak.likes.remove(request.user.id)
#             croak.save()
#         else:
#             croak.likes.add(request.user.id)
#             croak.save()

#         # save stuff to db
#         return render(
#             request, "partials/_like_htmx.html", {"croak": croak, "liked": liked}
#         )
