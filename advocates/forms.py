from django import forms
from .models import Advocate, AdvocateAvailability, AdvocateDocument

class AdvocateProfileForm(forms.ModelForm):
    class Meta:
        model = Advocate
        fields = [
            'bar_council_id', 'specializations', 'experience', 
            'consultation_fee', 'court_appearance_fee', 'bio', 
            'languages', 'education', 'certifications', 'is_available'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specializations': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class AdvocateAvailabilityForm(forms.ModelForm):
    class Meta:
        model = AdvocateAvailability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

