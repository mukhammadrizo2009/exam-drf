from rest_framework import generics, permissions, filters
from apps.users.permissions import IsDoctor
from apps.doctors.models import DoctorProfile
from apps.doctors.serializers import DoctorProfileSerializer, DoctorListSerializer
from django_filters.rest_framework import DjangoFilterBackend




class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsDoctor]

    def get_object(self):
        return DoctorProfile.objects.get(user=self.request.user)


class DoctorListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.select_related('user')
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        'user__username',
        'specialization',
    ]

    filterset_fields = [
        'specialization',
        'gender',
    ]

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = DoctorProfile.objects.select_related('user')
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticated]
