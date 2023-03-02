import pytest
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from umealse.models import Event
from taggit.models import Tag


class EventListTestCase(TestCase):
    """Tests for event_list endpoint."""

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        self.event = Event.objects.create(
            title="Test Event",
            slug="test-event",
            host=self.user,
            body="Test event",
            status=Event.Status.PUBLISHED,
        )
        self.event.tags.add(self.tag)
        self.url = reverse("event_list")

    def tearDown(self) -> None:
        self.user.delete()
        self.event.delete()

    def test_event_list(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next={self.url}")

        self.client.login(username="testuser", password="testpass")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/list.html")

    def test_event_list_with_tag(self) -> None:
        url = reverse("event_list_by_tag", args=[self.tag.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next={url}")

        self.client.login(username="testuser", password="testpass")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/list.html")


class EventDetailTestCase(TestCase):
    """Tests for event_detail endpoint."""

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.event = Event.objects.create(
            title="Test Event",
            slug="test-event",
            host=self.user,
            body="Test description",
            status=Event.Status.PUBLISHED,
        )
        self.url = reverse("event_detail", args=[self.event.id])

    def tearDown(self) -> None:
        self.user.delete()
        self.event.delete()

    def test_event_detail(self) -> None:
        """Ensure logged in user can see event's details."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next={self.url}")

        self.client.login(username="testuser", password="testpass")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/detail.html")
        self.assertContains(response, "Test Event")

    def test_event_detail_invalid_id(self) -> None:
        """Ensure 404 is returned when user asks for non-existant event."""
        url = reverse("event_detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next={url}")

        self.client.login(username="testuser", password="testpass")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class EventAddTestCase(TestCase):
    """Tests for event_add endpoint."""

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = reverse("add_event")

    def tearDown(self) -> None:
        self.user.delete()
        Event.objects.all().delete()

    def test_event_add(self) -> None:
        """Ensure logged in user can create a new event."""
        data = {
            "title": "Test Event",
            "body": "You are welcome to join this event.",
            "event_date": datetime.datetime.now() + datetime.timedelta(days=10),
            "private": False,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next={self.url}")

        self.client.login(username="testuser", password="testpass")

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertRedirects(response, f"/event/{event.id}")
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.host, self.user)
        self.assertEqual(event.attendees.count(), 0)
