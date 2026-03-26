from django.urls import path
from .views import SignUpView, UserProfileDetailView, UserProfileUpdateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/<int:pk>/", UserProfileDetailView.as_view(), name="profile_detail"),
    path("profile/<int:pk>/edit", UserProfileUpdateView.as_view(), name="profile_edit"),
]
