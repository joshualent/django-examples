from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

# Create your views here.


class HomePageView(TemplateView):
    """Home Page View"""

    template_name = "home.html"


def custom_403_view(request, exception):
    """Custom 403 Handling"""
    # NOTE: This is a function based view. You should not use
    # these except for this
    messages.add_message(
        request,
        messages.INFO,
        "You shall not pass!",
    )
    return redirect("home")
