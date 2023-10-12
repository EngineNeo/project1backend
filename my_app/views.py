from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rental, Film, Actor, Customer
from .serializers import FilmSerializer, ActorSerializer, CustomerSerializer, RentalSerializer
from django.db.models import Q

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
        
        actors_with_movies = []
        for actor in top_actors:
            actor_movies = (
                Film.objects.filter(filmactor__actor=actor)
                .annotate(rental_count=Count('inventory__rental'))
                .order_by('-rental_count')[:5]
            )
            actor_data = ActorSerializer(actor).data
            actor_data["top_movies"] = FilmSerializer(actor_movies, many=True).data
            actors_with_movies.append(actor_data)
        
        return Response(actors_with_movies)

class CustomerListView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        queryset = Customer.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        first_name = self.request.query_params.get('first_name')
        last_name = self.request.query_params.get('last_name')

        filter_conditions = Q()

        if customer_id:
            filter_conditions &= Q(customer_id=customer_id)

        if first_name:
            filter_conditions &= Q(first_name__icontains=first_name)

        if last_name:
            filter_conditions &= Q(last_name__icontains=last_name)

        # Apply the filter conditions to the queryset
        queryset = queryset.filter(filter_conditions)

        return queryset


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RentalListView(generics.ListAPIView):
    serializer_class = RentalSerializer

    def get_queryset(self):
        queryset = Rental.objects.all().order_by('rental_date')
        customer_id = self.request.query_params.get('customer_id')

        if customer_id:
            customer = get_object_or_404(Customer, customer_id=customer_id)
            queryset = queryset.filter(customer=customer).select_related('inventory__film')

        return queryset


class FilmListView(generics.ListAPIView):
    serializer_class = FilmSerializer

    def get_queryset(self):
        queryset = Film.objects.all()
        film_name = self.request.query_params.get('film_name')
        actor_name = self.request.query_params.get('actor_name')
        genre = self.request.query_params.get('genre')

        filter_conditions = Q()

        if film_name:
            filter_conditions &= Q(title__icontains=film_name)

        if actor_name:
            # Assuming 'filmactor' is the related name for the ManyToMany field with Actor
            filter_conditions &= Q(filmactor__actor__first_name__icontains=actor_name) | \
                                Q(filmactor__actor__last_name__icontains=actor_name)

        if genre:
            filter_conditions &= Q(genre__icontains=genre)

        # Apply the filter conditions to the queryset
        queryset = queryset.filter(filter_conditions)

        return queryset