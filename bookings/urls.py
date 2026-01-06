from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:advocate_id>/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('review/<int:booking_id>/', views.create_review, name='create_review'),
    path('update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]