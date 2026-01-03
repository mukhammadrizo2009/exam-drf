from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.permissions import IsDoctor, IsPatient, IsAdmin
from .models import TimeSlot, Appointment
from .serializers import (
    TimeSlotSerializer,
    AppointmentCreateSerializer,
    AppointmentListSerializer,
    AppointmentUpdateSerializer,
)


class TimeSlotCreateView(generics.CreateAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class TimeSlotListView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return TimeSlot.objects.filter(
            doctor=self.request.user
        )

class TimeSlotDeleteView(generics.DestroyAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return TimeSlot.objects.filter(
            doctor=self.request.user,
            is_available=True
        )

class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsPatient]

class MyAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        user = self.request.user

        qs = Appointment.objects.select_related(
            'doctor',
            'patient',
            'timeslot'
        )

        if user.role == 'doctor':
            return qs.filter(doctor=user)

        if user.role == 'patient':
            return qs.filter(patient=user)

        return qs
    
class AppointmentUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [IsDoctor | IsAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.all()

        if user.role == 'doctor':
            return qs.filter(doctor=user)

        return qs

class AppointmentDeleteView(generics.DestroyAPIView):

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.select_related('timeslot')

        if user.role == 'patient':
            return qs.filter(patient=user)

        if user.role == 'admin':
            return qs

        return qs.none()

    def perform_destroy(self, instance):
        instance.timeslot.is_available = True
        instance.timeslot.save()
        instance.delete()

class AdminAppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.select_related(
        'doctor', 'patient', 'timeslot'
    )
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAdmin]

class MyAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.select_related(
            'doctor', 'patient', 'timeslot'
        )

        if user.role == 'doctor':
            return qs.filter(doctor=user)

        if user.role == 'patient':
            return qs.filter(patient=user)

        return qs
