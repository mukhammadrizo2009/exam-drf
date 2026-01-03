from rest_framework import generics, permissions
from apps.users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from apps.users.permissions import IsPatient, IsAdmin
from apps.users.models import PatientProfile
from apps.users.serializers import PatientProfileSerializer, UserAdminSerializer


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user

class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        return PatientProfile.objects.get(user=self.request.user)
    
class UserAdminListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]


class UserAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]
