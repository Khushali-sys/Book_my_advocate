from rest_framework import serializers
from accounts.models import User
from advocates.models import Advocate, Specialization
from bookings.models import Booking, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'phone']
        read_only_fields = ['id']

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class AdvocateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Advocate
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    advocate = AdvocateSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'

