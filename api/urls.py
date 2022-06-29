from django.urls import path
from api import api_view
from api import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('medibot/', api_view.MediBotAPIView.as_view(), name='medibot'),
    path('heart-disease-model/', api_view.HeartDiseaseAPIView.as_view(), name='heart_disease_model'),
    path('diagnose/', api_view.DiagnoseAPIView.as_view(), name='diagnose'),
    path('appointment/', api_view.AppointmentCreateAPIView.as_view(), name='appointment'),
]
