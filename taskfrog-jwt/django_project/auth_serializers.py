from dj_rest_auth.serializers import PasswordResetSerializer
from .auth_forms import CustomAllAuthPasswordResetForm


class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = CustomAllAuthPasswordResetForm
