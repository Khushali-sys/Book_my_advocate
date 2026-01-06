from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import AdvocateViewSet, SpecializationViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'advocates', AdvocateViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]

