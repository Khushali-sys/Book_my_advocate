from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from advocates.models import Advocate

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    )
    
    SERVICE_TYPE_CHOICES = (
        ('consultation', 'Legal Consultation'),
        ('court_appearance', 'Court Appearance'),
        ('document_review', 'Document Review'),
        ('legal_advice', 'Legal Advice'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )
    
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
    )
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration = models.IntegerField(default=60, help_text="Duration in minutes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    case_description = models.TextField()
    case_type = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-booking_date', '-booking_time']
        unique_together = ['advocate', 'booking_date', 'booking_time']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.client.username} with {self.advocate}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    professionalism = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    expertise = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.client.username} for {self.advocate}"
