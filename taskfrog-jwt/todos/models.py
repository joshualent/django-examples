from django.urls import reverse
from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo_detail", kwargs={"pk": self.pk})
