from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from advocates.models import Advocate, Specialization
from bookings.models import Booking, Review
from .serializers import (
    AdvocateSerializer, SpecializationSerializer,
    BookingSerializer, ReviewSerializer
)

class AdvocateViewSet(viewsets.ModelViewSet):
    queryset = Advocate.objects.filter(verified=True)
    serializer_class = AdvocateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experience', 'is_available', 'verified']
    search_fields = ['user__first_name', 'user__last_name', 'bio']
    ordering_fields = ['rating', 'total_cases', 'consultation_fee']
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        advocate = self.get_object()
        reviews = Review.objects.filter(advocate=advocate, is_verified=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'client':
            return Booking.objects.filter(client=user)
        elif user.user_type == 'advocate':
            return Booking.objects.filter(advocate__user=user)
        return Booking.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

