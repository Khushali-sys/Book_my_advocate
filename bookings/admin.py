from django.contrib import admin
from .models import Booking, Review

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'advocate', 'booking_date', 'booking_time', 'status', 'payment_status', 'total_fee']
    list_filter = ['status', 'payment_status', 'service_type', 'priority', 'booking_date']
    search_fields = ['client__username', 'advocate__user__username', 'case_type', 'case_description']
    date_hierarchy = 'booking_date'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'advocate', 'rating', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'rating', 'created_at']
    search_fields = ['client__username', 'advocate__user__username', 'comment']
