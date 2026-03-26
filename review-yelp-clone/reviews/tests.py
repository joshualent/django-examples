from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Restaurant, Review


class RestaurantTests(TestCase):
    """Restaurant Tests"""

    @classmethod
    def setUpTestData(cls):
        """Set up class test data"""
        cls.restaurant = Restaurant.objects.create(name="Business Name")

        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secure_pass123"
        )

        cls.review = Review.objects.create(
            restaurant=cls.restaurant, user=cls.user, body="Ok review", rating=3
        )

    def test_restaurant_model(self):
        """Test the Restaurant model works as intended"""
        self.assertEqual(self.restaurant.name, "Business Name")
        self.assertEqual(str(self.restaurant), "Business Name")

    def test_url_exists_at_correct_location_listview(self):
        """Test URL exists at correct location for the listview"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        """Test URL exists at correct location for the detailview"""
        response = self.client.get("/restaurant/1/")
        self.assertEqual(response.status_code, 200)

    def test_restaurant_listview(self):
        """Test Restaurant listview"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Restaurants")
        self.assertTemplateUsed(response, "home.html")

    def test_restaurant_detailview(self):
        """test restaurant detailview"""
        response = self.client.get(
            reverse("restaurant_detail", kwargs={"pk": self.restaurant.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.review.user.username)
        self.assertContains(response, f"⭐{self.review.rating}-Star")
        self.assertContains(response, self.review.user.username)
        self.assertTemplateUsed(response, "restaurant_detail.html")


class ReviewTests(TestCase):
    """Review Tests"""

    @classmethod
    def setUpTestData(cls):
        """Set up class test data"""
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secure_pass123"
        )
        cls.restaurant = Restaurant.objects.create(name="Business Name")
        cls.review = Review.objects.create(
            restaurant=cls.restaurant, user=cls.user, body="Ok review", rating=3
        )

    def test_review_model(self):
        """Test the Review model works as intended"""
        self.assertEqual(self.review.body, "Ok review")
        self.assertEqual(str(self.review), "3-Star | Ok review")
        self.assertEqual(self.review.user.username, "testuser")

    def test_url_exists_at_correct_location_listview(self):
        """Test URL exists at correct location for the listview"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        """Test URL exists at correct location for the detailview"""
        response = self.client.get("/review/1/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_updateview(self):
        """Test URL exists at correct location for the updateview"""
        response = self.client.get("/review/1/edit/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_deleteview(self):
        """Test URL exists at correct location for the deleteview"""
        response = self.client.get("/review/1/delete/")
        self.assertEqual(response.status_code, 200)

    def test_review_detailview(self):
        """Test Review DetailView"""
        response = self.client.get(
            reverse("review_detail", kwargs={"pk": self.review.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.body)
        self.assertTemplateUsed(response, "review_detail.html")

    def test_review_createview(self):
        """Test Review CreateView"""
        data = {
            "user": self.user,
            "rating": 4,
            "restaurant": self.restaurant,
            "body": "Pretty good food. Enjoyable.",
        }
        response = self.client.post(reverse("review_new"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "review_new.html")

    def test_review_updateview(self):
        """Test Review UpdateView"""
        data = {
            "user": self.user,
            "rating": 4,
            "restaurant": self.restaurant,
            "body": "Pretty good food. Enjoyable.",
        }
        response = self.client.post(
            reverse("review_edit", kwargs={"pk": self.review.pk}),
            data=data,
            follow=True,
        )

        review = Review.objects.all().first()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "review_detail.html")
        self.assertEqual(review.body, "Pretty good food. Enjoyable.")
        self.assertEqual(review.user.username, "testuser")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.restaurant, self.restaurant)
