from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.doctors.models import DoctorProfile
from apps.users.models import PatientProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'role')

    def create(self, validated_data):
        role = validated_data.get('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role
        )

        if role == 'doctor':
            DoctorProfile.objects.create(
                user=user,
                specialization='',
                experience_years=0,
                gender='male'
            )

        if role == 'patient':
            PatientProfile.objects.create(
                user=user,
                phone='',
                date_of_birth='2000-01-01',
                gender='male'
            )

        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = (
            'id',
            'phone',
            'date_of_birth',
            'gender',
        )
        


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'role',
            'is_active',
            'created_at',
        )
