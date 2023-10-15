from django.db.models import Count
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rental, Film, Actor, Customer, Address, Inventory
from .serializers import ( FilmSerializer, ActorSerializer, 
                          CustomerSerializer, RentalSerializer, AddressSerializer,
                          InventorySerializer)
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .forms import RentalForm

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
        email = self.request.query_params.get('email', None)

        if email is not None:
            queryset = queryset.filter(email__icontains=email)

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
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            filter_conditions &= Q(filmactor__actor__first_name__icontains=actor_name) | \
                                Q(filmactor__actor__last_name__icontains=actor_name)

        if genre:
            # Adjusted the genre filter to work through the FilmCategory model
            filter_conditions &= Q(filmcategory__category__name__icontains=genre)

        # Apply the filter conditions to the queryset
        queryset = queryset.filter(filter_conditions)

        return queryset
    
class AddressListView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AvailableFilmsView(APIView):
    def get(self, request, film_id=None):
        rented_film_ids = Rental.objects.filter(return_date__isnull=True).values_list('inventory__film', flat=True)
        
        if film_id:
            available_films = Inventory.objects.filter(film_id=film_id).exclude(film__in=rented_film_ids).annotate(rental_count=Count('rental'))
        else:
            available_films = Inventory.objects.exclude(film__in=rented_film_ids).select_related('film').annotate(rental_count=Count('rental'))
        
        serializer = InventorySerializer(available_films, many=True)
        return Response(serializer.data)

def create_rental(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rental_success')
    else:
        form = RentalForm()

    return render(request, 'create_rental.html', {'form': form})

@api_view(['POST'])
def rent_film_api(request):
    if request.method == 'POST':
        email = request.data.get('email')
        film_id = request.data.get('film_id')

        # Get the customer from the email
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Set a default staff_id
        staff_id = 1

        # Find an available inventory_id for the specified film_id
        try:
            inventory = Inventory.objects.filter(film_id=film_id).first()
        except Inventory.DoesNotExist:
            return Response({'error': 'No available inventory for specified film'}, status=status.HTTP_400_BAD_REQUEST)

        if not inventory:
            return Response({'error': 'No available inventory for specified film'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the film to calculate the return date
        film = inventory.film
        rental_duration = timedelta(days=film.rental_duration)
        rental_date = timezone.now()
        return_date = rental_date + rental_duration

        # Create a new Rental instance
        rental = Rental(
            rental_date=rental_date,
            inventory=inventory,
            customer=customer,
            return_date=return_date,
            staff_id=staff_id,
            last_update=rental_date,  # Set the last update to the current timestamp
        )
        rental.save()

        return Response({'message': 'Film rented successfully'}, status=status.HTTP_201_CREATED)
