from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:id>/shows/', views.MovieShowsView.as_view(), name='movie-shows'),
    path('shows/<int:id>/book/', views.BookSeatView.as_view(), name='book-seat'),
    path('bookings/<int:id>/cancel/', views.CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),

    path('add-movie/', views.AddMoviesView.as_view(), name='add-movie'),
    path('add-show/', views.AddShowView.as_view(), name='add-show'),
]