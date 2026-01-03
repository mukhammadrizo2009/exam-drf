from django.contrib import admin
from apps.users.models import User, PatientProfile

admin.site.register(User)
admin.site.register(PatientProfile)