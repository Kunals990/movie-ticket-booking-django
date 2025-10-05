from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Show, Booking

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__' 

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    show_details = ShowSerializer(source='show', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'user', 'show','show_details', 'seat_number', 'status', 'created_at')
        extra_kwargs = {'show': {'write_only': True}}