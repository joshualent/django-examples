from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    AdminUserCreationForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomAdminUserCreationForm,
)
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    add_form = CustomAdminUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "age",
        "is_staff",
    ]
    new_fieldsets = ((None, {"fields": ("age",)}),)
    fieldsets = UserAdmin.fieldsets + new_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + new_fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
