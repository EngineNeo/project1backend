from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rental, Film, Actor, Customer, Rental
from .serializers import FilmSerializer, ActorSerializer, CustomerSerializer, RentalSerializer, FilmSerializer

class TopMoviesView(APIView):
    def get(self, request):
        top_movies = (
            Film.objects.annotate(
                rental_count=Count('inventory__rental')
            ).order_by('-rental_count')[:5]
        )
        serializer = FilmSerializer(top_movies, many=True)
        return Response(serializer.data)

class TopActorsView(APIView):
    def get(self, request):
        top_actors = (
            Actor.objects.annotate(
                rental_count=Count('filmactor__film__inventory__rental')
            ).order_by('-rental_count')[:5]
        )
        serializer = ActorSerializer(top_actors, many=True)
        return Response(serializer.data)

class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RentalListView(generics.ListAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class FilmListView(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer 