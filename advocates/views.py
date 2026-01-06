from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Advocate, Specialization, AdvocateAvailability
from bookings.models import Review
from .forms import AdvocateProfileForm, AdvocateAvailabilityForm

def advocate_list(request):
    advocates = Advocate.objects.filter(verified=True, is_available=True).select_related('user')
    
    # Search
    search = request.GET.get('search')
    if search:
        advocates = advocates.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(specializations__name__icontains=search) |
            Q(bio__icontains=search)
        ).distinct()
    
    # Filter by specialization
    specialization_id = request.GET.get('specialization')
    if specialization_id:
        advocates = advocates.filter(specializations__id=specialization_id)
    
    # Filter by experience
    experience = request.GET.get('experience')
    if experience:
        advocates = advocates.filter(experience=experience)
    
    # Filter by rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        advocates = advocates.filter(rating__gte=min_rating)
    
    # Sort
    sort_by = request.GET.get('sort_by', '-rating')
    advocates = advocates.order_by(sort_by)
    
    specializations = Specialization.objects.all()
    
    context = {
        'advocates': advocates,
        'specializations': specializations,
    }
    return render(request, 'advocates/advocate_list.html', context)

def advocate_detail(request, advocate_id):
    advocate = get_object_or_404(Advocate.objects.select_related('user'), id=advocate_id)
    reviews = Review.objects.filter(advocate=advocate, is_verified=True).select_related('client')[:10]
    availability = AdvocateAvailability.objects.filter(advocate=advocate, is_available=True)
    
    # Calculate average ratings
    avg_ratings = reviews.aggregate(
        avg_professionalism=Avg('professionalism'),
        avg_communication=Avg('communication'),
        avg_expertise=Avg('expertise')
    )
    
    context = {
        'advocate': advocate,
        'reviews': reviews,
        'availability': availability,
        'avg_ratings': avg_ratings,
    }
    return render(request, 'advocates/advocate_detail.html', context)

@login_required
def advocate_profile_edit(request):
    if request.user.user_type != 'advocate':
        messages.error(request, 'Only advocates can access this page.')
        return redirect('dashboard')
    
    advocate, created = Advocate.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AdvocateProfileForm(request.POST, instance=advocate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('advocate_profile_edit')
    else:
        form = AdvocateProfileForm(instance=advocate)
    
    return render(request, 'advocates/profile_edit.html', {'form': form})
