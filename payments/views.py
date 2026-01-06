# ==========================================
# FILE: payments/views.py (Complete Version)
# ==========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from bookings.models import Booking
from .models import Payment
import uuid

@login_required
def initiate_payment(request, booking_id):
    """Initiate payment process for a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user has permission
    if booking.client != request.user:
        messages.error(request, 'You do not have permission to make payment for this booking.')
        return redirect('dashboard')
    
    # Check if already paid
    if booking.payment_status == 'paid':
        messages.info(request, 'This booking has already been paid for.')
        return redirect('booking_detail', booking_id=booking.id)
    
    context = {
        'booking': booking,
    }
    return render(request, 'payments/initiate_payment.html', context)


@login_required
def process_payment(request, booking_id):
    """Process the payment"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.client != request.user:
        messages.error(request, 'Unauthorized access.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Create or get payment
        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                'amount': booking.total_fee,
                'payment_method': payment_method,
                'transaction_id': str(uuid.uuid4()),
                'status': 'processing'
            }
        )
        
        # Simulate payment processing
        # In production, integrate with payment gateway (Razorpay, Stripe, etc.)
        try:
            # Payment gateway integration would go here
            # For now, we'll simulate successful payment
            
            payment.status = 'completed'
            payment.payment_date = timezone.now()
            payment.save()
            
            # Update booking
            booking.payment_status = 'paid'
            booking.status = 'confirmed'
            booking.save()
            
            messages.success(request, 'Payment completed successfully! Your booking is confirmed.')
            return redirect('payments:payment_success', booking_id=booking.id)
            
        except Exception as e:
            # Handle payment failure
            payment.status = 'failed'
            payment.notes = str(e)
            payment.save()
            
            messages.error(request, 'Payment failed. Please try again.')
            return redirect('payments:payment_failure', booking_id=booking.id)
    
    return redirect('payments:initiate_payment', booking_id=booking_id)


@login_required
def payment_success(request, booking_id):
    """Payment success confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.client != request.user:
        messages.error(request, 'Unauthorized access.')
        return redirect('dashboard')
    
    payment = get_object_or_404(Payment, booking=booking)
    
    context = {
        'booking': booking,
        'payment': payment,
    }
    return render(request, 'payments/payment_success.html', context)


@login_required
def payment_failure(request, booking_id):
    """Payment failure page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.client != request.user:
        messages.error(request, 'Unauthorized access.')
        return redirect('dashboard')
    
    try:
        payment = Payment.objects.get(booking=booking)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'booking': booking,
        'payment': payment,
    }
    return render(request, 'payments/payment_failure.html', context)


@login_required
def payment_details(request, payment_id):
    """View detailed payment information"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Check permissions
    if payment.booking.client != request.user and payment.booking.advocate.user != request.user:
        messages.error(request, 'You do not have permission to view this payment.')
        return redirect('dashboard')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_details.html', context)


@login_required
def payment_history(request):
    """View all payments for the logged-in user"""
    if request.user.user_type == 'client':
        payments = Payment.objects.filter(booking__client=request.user).select_related('booking').order_by('-created_at')
    elif request.user.user_type == 'advocate':
        payments = Payment.objects.filter(booking__advocate__user=request.user).select_related('booking').order_by('-created_at')
    else:
        payments = Payment.objects.all().select_related('booking').order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/payment_history.html', context)


@login_required
def request_refund(request, payment_id):
    """Request a refund for a payment"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Check if user is the client who made the payment
    if payment.booking.client != request.user:
        messages.error(request, 'You do not have permission to request a refund for this payment.')
        return redirect('dashboard')
    
    # Check if payment is eligible for refund
    if payment.status != 'completed':
        messages.error(request, 'This payment is not eligible for refund.')
        return redirect('payments:payment_details', payment_id=payment.id)
    
    if payment.status == 'refunded':
        messages.info(request, 'This payment has already been refunded.')
        return redirect('payments:payment_details', payment_id=payment.id)
    
    if request.method == 'POST':
        refund_reason = request.POST.get('reason', '')
        
        # Process refund
        # In production, integrate with payment gateway for actual refund
        payment.status = 'refunded'
        payment.refund_date = timezone.now()
        payment.refund_amount = payment.amount
        payment.notes = f"Refund requested. Reason: {refund_reason}"
        payment.save()
        
        # Update booking
        payment.booking.payment_status = 'refunded'
        payment.booking.status = 'cancelled'
        payment.booking.cancellation_reason = f"Refund requested: {refund_reason}"
        payment.booking.save()
        
        messages.success(request, 'Refund request submitted successfully. Amount will be credited within 5-7 business days.')
        return redirect('payments:payment_details', payment_id=payment.id)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/request_refund.html', context)