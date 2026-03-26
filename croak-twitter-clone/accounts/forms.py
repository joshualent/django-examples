from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AdminUserCreationForm,
)

from .models import CustomUser


class CustomAdminUserCreationForm(AdminUserCreationForm):
    """Custom User Creation Form"""

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")


class CustomUserCreationForm(UserCreationForm):
    """Custom User Creation Form"""

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")


class CustomUserChangeForm(UserChangeForm):
    """Custom User Change Form"""

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")
