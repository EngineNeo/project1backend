from django.urls import reverse, resolve
from my_app.views import CustomerListView
from django.test import TestCase

# Define the test case class
class TestCustomersURL(TestCase):
    def test_customer_list_url_resolves_correct_view(self):
        url = reverse('customer-list')  # Use 'customer-list' instead of 'customers'
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CustomerListView)