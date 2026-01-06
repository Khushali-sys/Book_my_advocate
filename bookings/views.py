from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, Review
from advocates.models import Advocate
from .forms import BookingForm, ReviewForm

@login_required
def create_booking(request, advocate_id):
    advocate = get_object_or_404(Advocate, id=advocate_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.advocate = advocate
            
            # Calculate fee based on service type
            if booking.service_type == 'consultation':
                booking.total_fee = advocate.consultation_fee
            elif booking.service_type == 'court_appearance':
                booking.total_fee = advocate.court_appearance_fee
            else:
                booking.total_fee = advocate.consultation_fee
            
            booking.save()
            messages.success(request, 'Booking created successfully! Please proceed to payment.')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'advocate': advocate,
    }
    return render(request, 'bookings/create_booking.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user has permission to view this booking
    if booking.client != request.user and booking.advocate.user != request.user:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('dashboard')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def my_bookings(request):
    if request.user.user_type == 'client':
        bookings = Booking.objects.filter(client=request.user).select_related('advocate__user')
    elif request.user.user_type == 'advocate':
        bookings = Booking.objects.filter(advocate__user=request.user).select_related('client')
    else:
        bookings = Booking.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.client != request.user:
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('dashboard')
    
    if booking.status in ['completed', 'cancelled']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.cancellation_reason = request.POST.get('reason', '')
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('my_bookings')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

@login_required
def create_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.client != request.user or booking.status != 'completed':
        messages.error(request, 'You cannot review this booking.')
        return redirect('dashboard')
    
    if hasattr(booking, 'review'):
        messages.info(request, 'You have already reviewed this booking.')
        return redirect('booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.advocate = booking.advocate
            review.client = request.user
            review.save()
            
            # Update advocate rating
            avg_rating = Review.objects.filter(advocate=booking.advocate).aggregate(Avg('rating'))['rating__avg']
            booking.advocate.rating = round(avg_rating, 2)
            booking.advocate.total_reviews = Review.objects.filter(advocate=booking.advocate).count()
            booking.advocate.save()
            
            messages.success(request, 'Review submitted successfully!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'bookings/create_review.html', context)

@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only advocate can update booking status
    if request.user.user_type != 'advocate' or booking.advocate.user != request.user:
        messages.error(request, 'You do not have permission to update this booking.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.notes = request.POST.get('notes', booking.notes)
            booking.save()
            messages.success(request, f'Booking status updated to {new_status}.')
            return redirect('booking_detail', booking_id=booking.id)
    
    return redirect('booking_detail', booking_id=booking.id)

