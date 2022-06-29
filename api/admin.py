from django.contrib import admin
from api.models import *


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'specialty', 'experience', 'telephone']
    search_fields = ['id', 'first_name', 'last_name', 'specialty']


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['id', 'specialty']
    search_fields = ['specialty']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'date_time']
    search_fields = ['id', 'doctor', 'date_time']

