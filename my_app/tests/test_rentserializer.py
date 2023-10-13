from django.test import TestCase
from my_app.models import Actor, Film, Customer, Rental, Address, Inventory
from my_app.serializers import RentalSerializer
import datetime

class RentalSerializerTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.actor = Actor.objects.create(actor_id=1, first_name="John", last_name="Doe")
        self.film = Film.objects.create(film_id=1, title="Film Title")
        self.customer = Customer.objects.create(customer_id=1, first_name="Alice", last_name="Smith")
        self.inventory = Inventory.objects.create(inventory_id=1, film=self.film, store_id=1, last_update=datetime.now())
        self.rental = Rental.objects.create(rental_id=1, rental_date="2023-01-01", return_date="2023-01-05", inventory=self.inventory)

    def test_rental_serializer(self):
        serializer = RentalSerializer(instance=self.rental)
        expected_data = {
            'rental_id': 1,
            'rental_date': '2023-01-01',
            'return_date': '2023-01-05',
            'film_title': 'Test Film'
        }
        self.assertEqual(serializer.data, expected_data)
        pass
