from rest_framework import serializers
from django.utils import timezone
from .models import TimeSlot, Appointment


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = (
            'id',
            'date',
            'start_time',
            'end_time',
            'is_available',
        )
        read_only_fields = ('is_available',)

    def validate(self, data):
        request = self.context['request']
        doctor = request.user

        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(
                "start_time end_time dan kichik bo'lishi kerak"
            )

        overlap = TimeSlot.objects.filter(
            doctor=doctor,
            date=data['date'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
        ).exists()

        if overlap:
            raise serializers.ValidationError(
                "Bu vaqt oralig'ida boshqa TimeSlot mavjud"
            )

        if data['date'] < timezone.now().date():
            raise serializers.ValidationError(
                "O'tmishdagi sana uchun TimeSlot yaratib bo'lmaydi"
            )

        return data

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'timeslot')

    def validate(self, data):
        request = self.context['request']
        user = request.user
        timeslot = data['timeslot']

        if user.role != 'patient':
            raise serializers.ValidationError(
                "Faqat patient appointment bron qila oladi"
            )
            
        if timeslot.doctor == user:
            raise serializers.ValidationError(
                "Doctor o'ziga appointment bron qila olmaydi"
            )

        if not timeslot.is_available:
            raise serializers.ValidationError(
                "Bu TimeSlot band qilingan"
            )

        if timeslot.date < timezone.now().date():
            raise serializers.ValidationError(
                "O'tmishdagi vaqtga appointment bron qilib bo'lmaydi"
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        timeslot = validated_data['timeslot']

        appointment = Appointment.objects.create(
            doctor=timeslot.doctor,
            patient=user,
            timeslot=timeslot
        )

        timeslot.is_available = False
        timeslot.save()

        return appointment

class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username')
    patient = serializers.CharField(source='patient.username')
    date = serializers.DateField(source='timeslot.date')
    start_time = serializers.TimeField(source='timeslot.start_time')
    end_time = serializers.TimeField(source='timeslot.end_time')

    class Meta:
        model = Appointment
        fields = (
            'id',
            'doctor',
            'patient',
            'date',
            'start_time',
            'end_time',
            'status',
            'created_at',
        )

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('status',)

    def validate_status(self, value):
        if value not in ['confirmed', 'cancelled']:
            raise serializers.ValidationError(
                "Faqat confirmed yoki cancelled bo'lishi mumkin"
            )
        return value

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('status',)

    def validate_status(self, value):
        if value not in ['confirmed', 'cancelled']:
            raise serializers.ValidationError(
                "Faqat confirmed yoki cancelled bo'lishi mumkin"
            )
        return value
