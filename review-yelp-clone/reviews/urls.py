from django.urls import path

from .views import (
    RestaurantListView,
    RestaurantDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewDetailView,
)

urlpatterns = [
    path("review/new/", ReviewCreateView.as_view(), name="review_new"),
    path("review/<int:pk>/edit/", ReviewUpdateView.as_view(), name="review_edit"),
    path("review/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review_delete"),
    path("review/<int:pk>/", ReviewDetailView.as_view(), name="review_detail"),
    path(
        "restaurant/<int:pk>/", RestaurantDetailView.as_view(), name="restaurant_detail"
    ),
    path("", RestaurantListView.as_view(), name="home"),
]
