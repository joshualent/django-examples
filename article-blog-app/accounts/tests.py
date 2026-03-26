from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


class SignUpPageTests(TestCase):
    """Sign Up Page Tests"""

    def test_url_exists_at_correct_location(self):
        """Test URL exists at correct location"""
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        """Test sign up view name"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        """Test signup form"""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        first_user = users[0]
        self.assertEqual(
            users.count(),
            1,
        )
        self.assertEqual(
            first_user.email,
            "testuser@email.com",
        )
        self.assertEqual(
            first_user.username,
            "testuser",
        )
