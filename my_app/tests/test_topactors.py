from django.urls import reverse, resolve
from my_app.views import TopActorsView
from django.test import TestCase

# Define the test case class
class TestTopActorsURL(TestCase):
    def test_top_movies_url_resolves_correct_view(self):
        # Define the URL name you want to test
        url = reverse('top-actors')
        # Use the resolve function to determine which view function is associated with the URL
        resolver = resolve(url)
        # Check if the resolved view function is the expected one (TopActorsView in this case)
        self.assertEqual(resolver.func.view_class, TopActorsView)
