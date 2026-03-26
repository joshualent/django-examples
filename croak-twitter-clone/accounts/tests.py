from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


class CustomUserModelTests(TestCase):
    """Custom User Model Tests"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secure_pass123",
            date_of_birth="2000-1-1",
        )

    def test_custom_user_model(self):
        """Test the CustomUser Model works as expected"""

        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@email.com")
        self.assertEqual(self.user.date_of_birth, "2000-1-1")

    def test_custom_user_model_relations(self):
        """Test CustomUser Model related fields for new user"""

        self.assertEqual(len(self.user.authored_croaks.all()), 0)
        self.assertEqual(len(self.user.authored_comments.all()), 0)


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
                "date_of_birth": "2000-1-1",
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
        self.assertEqual(str(first_user.date_of_birth), "2000-01-01")
