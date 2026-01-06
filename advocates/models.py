from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Advocate(models.Model):
    EXPERIENCE_CHOICES = (
        ('0-2', '0-2 years'),
        ('3-5', '3-5 years'),
        ('6-10', '6-10 years'),
        ('10+', '10+ years'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='advocate_profile')
    bar_council_id = models.CharField(max_length=50, unique=True)
    specializations = models.ManyToManyField(Specialization, related_name='advocates')
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    court_appearance_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    bio = models.TextField()
    languages = models.CharField(max_length=200, help_text="Comma separated languages")
    education = models.TextField()
    certifications = models.TextField(blank=True)
    success_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    total_cases = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', '-total_cases']
    
    def __str__(self):
        return f"Adv. {self.user.get_full_name()}"
    
    def get_languages_list(self):
        return [lang.strip() for lang in self.languages.split(',')]


class AdvocateAvailability(models.Model):
    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['advocate', 'day_of_week', 'start_time']
        ordering = ['day_of_week', 'start_time']
        verbose_name_plural = 'Advocate Availabilities'
    
    def __str__(self):
        return f"{self.advocate} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class AdvocateDocument(models.Model):
    DOCUMENT_TYPES = (
        ('license', 'Bar Council License'),
        ('certificate', 'Certificate'),
        ('degree', 'Degree'),
        ('other', 'Other'),
    )
    
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document = models.FileField(upload_to='advocate_docs/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.advocate} - {self.get_document_type_display()}"

