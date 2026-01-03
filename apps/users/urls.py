from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, MeView, PatientProfileView, UserAdminListView, UserAdminDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('patient/profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('users/', UserAdminListView.as_view()),
    path('users/<int:pk>/', UserAdminDetailView.as_view()),
]
