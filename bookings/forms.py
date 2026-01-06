from django import forms
from .models import Booking, Review
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'service_type', 'booking_date', 'booking_time', 'duration', 
            'case_description', 'case_type', 'priority'
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'case_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe your case in detail'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 30, 'step': 30}),
            'case_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Criminal, Civil, Family'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < date.today():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'professionalism', 'communication', 'expertise']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Share your experience'}),
            'professionalism': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'communication': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'expertise': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }
        labels = {
            'professionalism': 'Professionalism (1-5)',
            'communication': 'Communication (1-5)',
            'expertise': 'Legal Expertise (1-5)',
        }

