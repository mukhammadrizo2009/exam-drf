from rest_framework import serializers
from .models import DoctorProfile


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = (
            'id',
            'specialization',
            'experience_years',
            'gender',
        )

class DoctorListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = DoctorProfile
        fields = (
            'id',
            'username',
            'specialization',
            'experience_years',
            'gender',
        )
