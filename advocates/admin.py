from django.contrib import admin
from .models import Specialization, Advocate, AdvocateAvailability, AdvocateDocument

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

@admin.register(Advocate)
class AdvocateAdmin(admin.ModelAdmin):
    list_display = ['user', 'bar_council_id', 'experience', 'rating', 'total_cases', 'verified', 'is_available']
    list_filter = ['verified', 'is_available', 'experience']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bar_council_id']
    filter_horizontal = ['specializations']

@admin.register(AdvocateAvailability)
class AdvocateAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['advocate', 'day_of_week', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available']

@admin.register(AdvocateDocument)
class AdvocateDocumentAdmin(admin.ModelAdmin):
    list_display = ['advocate', 'document_type', 'uploaded_at']
    list_filter = ['document_type']

