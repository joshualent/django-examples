from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Restaurant(models.Model):
    """Restaurant Django Model"""

    name = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)[:50]

    def get_absolute_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.pk})


class Review(models.Model):
    """Review Django Model"""

    class Ratings(models.IntegerChoices):
        """Integer Choices enum for rating field"""

        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()

    rating = models.IntegerField(choices=Ratings)  # pyright: ignore[reportArgumentType]
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.rating}-Star | {str(self.body)[:40]}"

    def get_absolute_url(self):
        return reverse("review_detail", kwargs={"pk": self.pk})
