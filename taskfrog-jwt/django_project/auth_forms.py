from django.conf import settings
from dj_rest_auth.forms import AllAuthPasswordResetForm


def custom_url_generator(request, user, temp_key):
    """
    Custom URL generator for password reset emails.
    This generates a URL that points to your frontend application
    where users can reset their password via the API.
    """
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
    return f"{frontend_url}/password-reset-confirm/{user.pk}/{temp_key}/"


class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        # Use our custom URL generator
        return super().save(request, url_generator=custom_url_generator, **kwargs)
