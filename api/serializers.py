from rest_framework import serializers
from api.models import Doctor, Appointment


class DoctorSerializer(serializers.ModelSerializer):
    """ Serialize the Doctor model """

    specialty = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', '__str__', 'specialty', 'first_name', 'last_name', 'get_experience', 'link']

    def get_specialty(self, obj):
        return obj.specialty.specialty


class AppointmentSerializer(serializers.ModelSerializer):
    """ Serialize the Appointment model """

    class Meta:
        model = Appointment
        fields = '__all__'
