from django.test import TestCase
from my_app.forms import RentalForm
from my_app.models import Rental, Inventory, Film, Store
import datetime

class RentalFormTestCase(TestCase):
    def test_invalid_data(self):
        form = RentalForm(data={
            'rental_date': datetime.date.today(),
            'return_date': datetime.date.today() - datetime.timedelta(days=1),  # return date before rental date
            # ... other model fields with valid data
        })
        self.assertFalse(form.is_valid())

    def test_missing_fields(self):
        form = RentalForm(data={})
        self.assertFalse(form.is_valid())
        # assuming 'return_date' is optional, we exclude it from the comparison
        required_fields = set([field.name for field in Rental._meta.get_fields() 
                            if not field.auto_created and not field.primary_key and not field.blank and field.name != 'return_date'])
        missing_fields = set(form.errors)
        self.assertEqual(required_fields, missing_fields)

    def test_labels(self):
        form = RentalForm()
        self.assertEqual(form.fields['rental_date'].label, 'Rental Date')
        self.assertEqual(form.fields['return_date'].label, 'Return Date')

    def test_form_save(self):
        form = RentalForm(data={
            'rental_date': datetime.date.today(),
            'return_date': datetime.date.today() + datetime.timedelta(days=1),
            # ... other model fields with valid data
        })
        if form.is_valid():
            rental = form.save()
            self.assertIsInstance(rental, Rental)
            self.assertEqual(rental.rental_date, datetime.date.today())
            self.assertEqual(rental.return_date, datetime.date.today() + datetime.timedelta(days=1))
            # ... assert other fields' data
