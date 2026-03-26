from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import CustomUser
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Sign Up View"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """User Profile Update View"""

    model = CustomUser
    template_name = "profile_edit.html"
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
    )

    def test_func(self):
        profile_user = self.get_object()
        return profile_user == self.request.user


class UserProfileDetailView(DetailView):
    """User Profile Detail View"""

    model = CustomUser
    template_name = "profile_detail.html"
