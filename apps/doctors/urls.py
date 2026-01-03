from django.urls import path
from .views import (
    DoctorProfileView,
    DoctorListView,
    DoctorDetailView,
)

urlpatterns = [
    path('profile/', DoctorProfileView.as_view()),

    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
]
