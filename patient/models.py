from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    DOB = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.firstname} - {self.lastname}'
    

class Treatment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class PaymentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, 
                                related_name='patientmedicalhistory')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient.firstname} - {self.patient.lastname}'
    

    class Meta:
        verbose_name_plural = 'Medical History'


