from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from django.db import transaction
from rest_framework.permissions import IsAdminUser
from .serializers import (
    UserSerializer,
    MovieSerializer,
    ShowSerializer,
    BookingSerializer,
)

class AddMoviesView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes =[IsAdminUser,IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class AddShowView(generics.CreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieShowsView(generics.ListAPIView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        movie_id = self.kwargs['id']
        return Show.objects.filter(movie_id=movie_id)

class BookSeatView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, id):
        seat_number = request.data.get('seat_number')

        if not seat_number or not isinstance(seat_number, int) or seat_number <= 0:
            return Response({'error': 'A valid seat number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                show = Show.objects.select_for_update().get(id=id)

                if seat_number > show.total_seats:
                    return Response({'error': f'Invalid seat number. Must be between 1 and {show.total_seats}.'}, status=status.HTTP_400_BAD_REQUEST)

                booked_seats_count = Booking.objects.filter(show=show, status='booked').count()
                if booked_seats_count >= show.total_seats:
                    return Response({'error': 'This show is fully booked.'}, status=status.HTTP_400_BAD_REQUEST)

                is_already_booked = Booking.objects.filter(show=show, seat_number=seat_number, status='booked').exists()
                if is_already_booked:
                    return Response({'error': 'This seat is already booked.'}, status=status.HTTP_400_BAD_REQUEST)

                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    seat_number=seat_number,
                )
                serializer = BookingSerializer(booking)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Show.DoesNotExist:
            return Response({'error': 'Show not found.'}, status=status.HTTP_404_NOT_FOUND)

class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            booking=Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if booking.user!= request.user:
            return Response({'error':'You do not have permission to cancel this booking.'}, status=status.HTTP_403_FORBIDDEN)
        
        booking.status = 'cancelled'
        booking.save()
        return Response({'message': 'Booking cancelled successfully.'}, status=status.HTTP_200_OK)

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)