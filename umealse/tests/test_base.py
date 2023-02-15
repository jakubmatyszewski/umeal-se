from django.test import TestCase
from django.urls import resolve
from pytest_django.asserts import assertTemplateUsed

from umealse.views import landing_page


class TestLandingPage(TestCase):
    def test_root_url_resolves_to_landing_page(self):
        found = resolve("/")
        assert found.func == landing_page

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        assertTemplateUsed(response, "landing_page.html")


class TestNavigation(TestCase):
    ...
