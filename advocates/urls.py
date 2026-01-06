from django.urls import path
from . import views

urlpatterns = [
    path('', views.advocate_list, name='advocate_list'),
    path('<int:advocate_id>/', views.advocate_detail, name='advocate_detail'),
    path('profile/edit/', views.advocate_profile_edit, name='advocate_profile_edit'),
]