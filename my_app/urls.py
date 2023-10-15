from django.urls import path
from . import views

urlpatterns = [
    path('top-movies/', views.TopMoviesView.as_view(), name='top-movies'),
    path('top-actors/', views.TopActorsView.as_view(), name='top-actors'),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('rentals/', views.RentalListView.as_view(), name='rental-list'),
    path('films/', views.FilmListView.as_view(), name='film-list'),
    path('addresses/', views.AddressListView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
    path('available-films/', views.AvailableFilmsView.as_view(), name='available_films'),
    path('available-films/<int:film_id>/', views.AvailableFilmsView.as_view()),
    path('create-rental/', views.create_rental, name='create_rental'),
    path('api/rent-film/', views.rent_film_api, name='rent_film_api'),
]
