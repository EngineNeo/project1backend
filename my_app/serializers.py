# serializers.py
from rest_framework import serializers
from .models import Actor, Film, Customer, Rental, Address

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    film_title = serializers.CharField(source='inventory.film.title', read_only=True)

    class Meta:
        model = Rental
        fields = ['rental_id', 'rental_date', 'return_date', 'film_title']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'