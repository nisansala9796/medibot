from django.db import models
from datetime import timedelta
from django.utils import timezone


class Specialty(models.Model):
    """ Holds the specialty details """
    specialty = models.CharField(max_length=50)
    desc = models.TextField()

    def __str__(self):
        return self.specialty


class Doctor(models.Model):
    """ Holds details of Doctors """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    experience = models.IntegerField()
    telephone = models.TextField(max_length=10)
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING)
    link = models.URLField()

    def __str__(self):
        return 'Dr. {} {}'.format(self.first_name, self.last_name)

    @property
    def get_experience(self):
        return '{} years'.format(self.experience)


class Appointment(models.Model):
    """ Holds appointment details """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField(null=True, blank=True, default=timezone.now() + timedelta(days=2))

    def __str__(self):
        return self.id




