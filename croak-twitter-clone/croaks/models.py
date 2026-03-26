from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Croak(models.Model):
    """Croak Model"""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_croaks",
    )
    body = models.TextField(blank=True)
    image_url = models.URLField(max_length=400, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_croaks",
        blank=True,
    )

    # Order Croaks by created in descending order when querying the database by default
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        """Comment string method"""
        return str(f"{self.author} - {str(self.body)[:50]}")

    def get_absolute_url(self):
        """Get absolute URL"""
        return reverse("croak_detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        """Get like url"""
        return reverse("croak_like", kwargs={"pk": self.pk})


class Comment(models.Model):
    """Comment Model"""

    croak = models.ForeignKey(Croak, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_comments",
    )
    body = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Comment string method"""
        return str(f"{self.author} - {str(self.body)[:50]}")
