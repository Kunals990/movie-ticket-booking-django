from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Movie, Show, Booking
from django.urls import reverse

class BookingLogicTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(movie=self.movie, screen_name='Screen 1', date_time='2025-10-06T19:00:00Z', total_seats=2)

    def _get_jwt_token_for_user(self, username='testuser', password='password123'):
        """Helper method to get a JWT token."""
        url = reverse('token_obtain_pair') 
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_successful_booking(self):
        """
        Ensure a logged-in user can successfully book an available seat.
        """
        token = self._get_jwt_token_for_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = f'/api/shows/{self.show.id}/book/'
        data = {'seat_number': 1}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().seat_number, 1)

    def test_prevent_double_booking(self):
        """
        Ensure the system prevents a seat from being booked twice.
        """
        Booking.objects.create(user=self.user, show=self.show, seat_number=1)
        
        token = self._get_jwt_token_for_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = f'/api/shows/{self.show.id}/book/'
        data = {'seat_number': 1}  #  attempt to book same seat again
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)

    def test_prevent_overbooking(self):
        """
        Ensure the system prevents booking more seats than available.
        """
        another_user = User.objects.create_user(username='user2', password='password123')
        Booking.objects.create(user=self.user, show=self.show, seat_number=1)
        Booking.objects.create(user=another_user, show=self.show, seat_number=2)

        token = self._get_jwt_token_for_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = f'/api/shows/{self.show.id}/book/'
        data = {'seat_number': 3} #attempt to book a third seat
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 2)
        
    def test_user_can_cancel_own_booking(self):
        """
        Ensure a user can cancel their own booking.
        """
        booking = Booking.objects.create(user=self.user, show=self.show, seat_number=1)
        
        token = self._get_jwt_token_for_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = f'/api/bookings/{booking.id}/cancel/'
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')