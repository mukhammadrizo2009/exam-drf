from django.urls import path
from .views import (
    TimeSlotCreateView,
    TimeSlotListView,
    TimeSlotDeleteView,
    AppointmentCreateView,
    MyAppointmentListView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    AdminAppointmentListView,
)

urlpatterns = [
    path('timeslots/', TimeSlotCreateView.as_view()),
    path('timeslots/me/', TimeSlotListView.as_view()),
    path('timeslots/<int:pk>/', TimeSlotDeleteView.as_view()),
    path('appointments/', AppointmentCreateView.as_view()),
    path('appointments/me/', MyAppointmentListView.as_view()),
    path('appointments/<int:pk>/', AppointmentUpdateView.as_view()),
    path('appointments/<int:pk>/cancel/', AppointmentDeleteView.as_view()),
    path('appointments/all/', AdminAppointmentListView.as_view()),
]
