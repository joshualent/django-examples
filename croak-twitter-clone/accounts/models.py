from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.
class CustomUser(AbstractUser):
    """Custom Auth User Model"""

    date_of_birth = models.DateField()

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})
