from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.


class HomePageTests(SimpleTestCase):
    """HomePageTests"""

    def test_url_at_correct_location(self):
        """Test URL at correct location"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        """Test homepage by name"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Home")
