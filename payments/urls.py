# ==========================================
# FILE: payments/urls.py
# ==========================================

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Initiate payment for a booking
    path('initiate/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    
    # Process payment
    path('process/<int:booking_id>/', views.process_payment, name='process_payment'),
    
    # Payment success page
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    
    # Payment failure page
    path('failure/<int:booking_id>/', views.payment_failure, name='payment_failure'),
    
    # View payment details
    path('details/<int:payment_id>/', views.payment_details, name='payment_details'),
    
    # Payment history for user
    path('history/', views.payment_history, name='payment_history'),
    
    # Request refund
    path('refund/<int:payment_id>/', views.request_refund, name='request_refund'),
]