from django.urls import path, include
from .views import TopMoviesView, TopActorsView, CustomerListView, CustomerDetailView, RentalListView, FilmListView

urlpatterns = [
    path('top-movies/', TopMoviesView.as_view(), name='top-movies'),
    path('top-actors/', TopActorsView.as_view(), name='top-actors'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('rentals/', RentalListView.as_view(), name='rental-list'),
    path('films/', FilmListView.as_view(), name='film-list'),
]