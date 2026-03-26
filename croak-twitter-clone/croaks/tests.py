from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Croak, Comment


class CroakTests(TestCase):
    """Croak and Comment Model Tests"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secure_pass123",
            date_of_birth="2000-1-1",
        )

        cls.croak = Croak.objects.create(
            author=cls.user,
            body="test croak",
            image_url="https://github.com/test.png",
        )

        cls.comment = Comment.objects.create(
            croak=cls.croak,
            author=cls.user,
            body="test comment",
        )

    def test_croak_model(self):
        """Test Croak model"""

        self.assertEqual(self.croak.author, self.user)
        self.assertEqual(len(self.croak.comments.all()), 1)
        self.assertEqual(self.croak.comments.all().first(), self.comment)
        self.assertEqual(len(self.croak.likes.all()), 0)

        self.assertEqual(self.croak.body, "test croak")
        self.assertEqual(self.croak.image_url, "https://github.com/test.png")

        self.assertEqual(str(self.croak), "testuser - test croak")

    def test_comment_model(self):
        """Test Comment model"""
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.croak, self.croak)
        self.assertEqual(self.comment.body, "test comment")

    def test_user_comments_and_croaks(self):
        """Test User's Croaks and Comments"""
        self.assertEqual(self.user.authored_croaks.all().first(), self.croak)
        self.assertEqual(self.user.authored_comments.all().first(), self.comment)
        self.assertEqual(len(self.user.liked_croaks.all()), 0)


class CroakViewTests(TestCase):
    """Croak View Tests"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="test",
            last_name="user",
            password="secure_pass123",
            date_of_birth="2000-1-1",
        )

        cls.croak = Croak.objects.create(
            author=cls.user,
            body="test croak",
            image_url="https://github.com/test.png",
        )

        cls.comment = Comment.objects.create(
            croak=cls.croak,
            author=cls.user,
            body="test comment",
        )

    def test_croak_createview(self):
        """Test Croak CreateView"""
        # login since view uses LoginRequiredMixin
        self.client.force_login(self.user)
        data = {
            "user": self.user,
            "body": "I just ate oatmeal",
        }
        response = self.client.post(reverse("croak_new"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "croak_detail.html")

    def test_croak_createview_requires_login(self):
        """Test Croak CreateView requires login"""
        response = self.client.get(reverse("croak_new"))
        self.assertEqual(response.status_code, 302)

    def test_url_exists_at_correct_location_croak_listview(self):
        """Test URL exists at correct location for the home/feed page"""

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_croak_listview(self):
        """Test the Home/Feed View"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Feed | Croak</title>")
        self.assertTemplateUsed(response, "croak_list.html")

    def test_croak_detailview_at_correct_location(self):
        """Test Croak DetailView at correct location"""
        self.client.force_login(self.user)
        response = self.client.get(f"/{self.croak.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_croak_detailview(self):
        """Test Croak DetailView"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("croak_detail", kwargs={"pk": self.croak.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="https://github.com/test.png"')

    def test_croak_updateview(self):
        """Test Croak UpdateView"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("croak_edit", kwargs={"pk": self.croak.pk}),
            {
                "body": "test croak edited",
            },
            follow=True,
        )
        croaks = Croak.objects.all()
        first_croak = croaks.first()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "croak_detail.html")

        self.assertEqual(croaks.count(), 1)
        self.assertEqual(first_croak.body, "test croak edited")

    def test_croak_updateview_requires_login(self):
        """Test Croak UpdateView requires login"""
        response = self.client.get(reverse("croak_edit", kwargs={"pk": self.croak.pk}))
        self.assertEqual(response.status_code, 302)

    def test_croak_deleteview(self):
        """Test Croak DeleteView"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("croak_delete", kwargs={"pk": self.croak.pk}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Croak.objects.all().count(), 0)

    def test_croak_deleteview_requires_login(self):
        """Test Croak DeleteView requires login"""
        response = self.client.get(
            reverse("croak_delete", kwargs={"pk": self.croak.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_comment_createview(self):
        """Test Croak CreateView (Croak DetailView)"""
        # login since view uses LoginRequiredMixin
        self.client.force_login(self.user)
        data = {
            "user": self.user,
            "body": "wow, cool!",
        }
        response = self.client.post(
            reverse("croak_detail", kwargs={"pk": self.croak.pk}),
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "croak_detail.html")
        self.assertContains(response, "wow, cool!")

    def test_comment_createview_requires_login(self):
        """Test Comment CreateView requires login"""
        response = self.client.get(
            reverse("croak_detail", kwargs={"pk": self.croak.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_profile_detailview(self):
        """Test profile DetailView"""
        response = self.client.get(
            reverse("profile_detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_detail.html")
        self.assertContains(response, "testuser")
        self.assertContains(response, "test user")
        self.assertContains(response, "1 Croak")
        self.assertContains(response, "testuser")
        self.assertContains(response, "test user")

    def test_profile_updateview(self):
        """Test Profile UpdateView"""

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("profile_edit", kwargs={"pk": self.user.pk}),
            {
                "username": "testuseredited",
                "email": "test@edited.com",
                "last_name": "useredited",
                "password": "secure_pass123",
                "date_of_birth": "2000-1-1",
            },
            follow=True,
        )
        users = get_user_model().objects.all()
        first_user = users.first()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_detail.html")

        self.assertEqual(users.count(), 1)
        self.assertEqual(first_user.username, "testuseredited")
        self.assertEqual(first_user.email, "test@edited.com")
