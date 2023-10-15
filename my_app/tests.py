from django.test import TestCase, Client
from django.urls import reverse
from .models import Film, Customer, Inventory, Rental
import json
from datetime import datetime

class RentMovieTestCase(TestCase):

    def setUp(self):
        # Create a test film, customer, and inventory item
        self.film = Film.objects.create(title="Test Movie", rental_rate=1.99)
        self.customer = Customer.objects.create(first_name="John", last_name="Doe")
        self.inventory = Inventory.objects.create(film=self.film)
        self.client = Client()

    def test_rent_movie(self):
        # Set up the data you're going to send with the POST request
        rental_data = {
            "rental_date": datetime.now(),
            "inventory": self.inventory.inventory_id,
            "customer": self.customer.customer_id,
            # Add any other required fields
        }

        # Assume 'rent_movie' is the URL name for your movie rental view
        response = self.client.post(reverse('rent_movie'), data=json.dumps(rental_data), content_type='application/json')

        # Check that the response is 201 CREATED, or another expected successful status code
        self.assertEqual(response.status_code, 201)

        # You could also add checks to ensure that the rental object was created in the database, etc.
