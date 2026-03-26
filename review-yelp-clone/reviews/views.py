from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Restaurant, Review
from django.urls import reverse_lazy

# Create your views here.


class RestaurantListView(ListView):
    """Restaurant List View"""

    model = Restaurant
    template_name = "home.html"


class RestaurantDetailView(DetailView):
    """Restaurant Detail View"""

    model = Restaurant
    template_name = "restaurant_detail.html"


class ReviewCreateView(CreateView):
    """Review Create View"""

    model = Review
    template_name = "review_new.html"
    fields = (
        "restaurant",
        "user",
        "rating",
        "body",
    )


class ReviewDetailView(DetailView):
    """Review Detail View"""

    model = Review
    template_name = "review_detail.html"


class ReviewUpdateView(UpdateView):
    """Review Update View"""

    model = Review
    template_name = "review_edit.html"
    fields = ("rating", "body")


class ReviewDeleteView(DeleteView):
    """Review DeleteView"""

    model = Review
    template_name = "review_delete.html"
    success_url = reverse_lazy("home")
