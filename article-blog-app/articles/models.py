from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Article(models.Model):
    """Article Model"""

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)  # allows blank string
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_articles", blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """String method"""
        return str(self.title)

    def get_absolute_url(self):
        """Get the absolute URL for the model."""
        return reverse("article_detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        """Get like url based on pk"""
        return reverse("article_like", kwargs={"pk": self.pk})


class Comment(models.Model):
    """Comment model"""

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String method"""
        return str(self.body)

    def get_absolute_url(self):
        """Get the absolute url for the model"""
        return reverse("article_list")
