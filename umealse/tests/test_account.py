from io import BytesIO
from PIL import Image

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from umealse.models import Profile


class AccountTestCase(TestCase):
    """Tests for functions related with pages under /account/ endpoints."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@user.com", password="testpass"
        )
        Profile.objects.create(user=self.user)

        self.user2 = User.objects.create_user(
            username="testuser_2", email="test@second.com", password="testpass"
        )
        Profile.objects.create(user=self.user2)

    @staticmethod
    def create_profile_pic() -> bytes:
        """Create picture for user profile."""

        im = Image.new(mode="RGB", size=(200, 200), color=(127, 127, 255))
        im_io = BytesIO()
        im.save(im_io, "JPEG")
        return im_io.getvalue()

    def test_dashboard(self) -> None:
        """Ensure Dashboard is assessible after user logs in."""

        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/dashboard/")

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard.html")

    def test_edit_profile(self) -> None:
        """Logged in user should be able to edit one's profile details."""

        url = reverse("edit_profile")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)

        self.client.login(username="testuser", password="testpass")

        picture_content = self.create_profile_pic()
        response = self.client.post(
            url,
            {
                "first_name": "Test",
                "email": "testuser@example.com",
                "profile.picture": SimpleUploadedFile(
                    name="test_image.jpg",
                    content=picture_content,
                    content_type="image/jpeg",
                ),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertIsNotNone(self.user.profile.photo)
        self.assertTemplateUsed(response, "account/edit_profile.html")

    def test_view_profile(self) -> None:
        """Logged in user should be able to view other users profiles."""

        url = reverse("profile", args=[self.user2.username])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username="testuser", password="testpass")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, "Add to friends")

        # checking self
        url = reverse("profile", args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
