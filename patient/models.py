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
    weight = models.IntegerField(default=0)
    BPressure = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.firstname} - {self.lastname}'
    

class Treatment(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.name} - {self.price}'
    
class ReviewofSystem(models.Model):
    name = models.CharField(max_length=255)
    

    def __str__(self):
        return f'{self.name}'
    

class Examination(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.name}'
    
class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    

    def __str__(self):
        return f'{self.name}'
    
class Investgation(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.name} - {self.price}'
    
class Medication(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.name} - {self.price}'
    
class Doctor(models.Model):
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
    # treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    history = models.CharField(max_length=255)
    review_of_systems = models.ManyToManyField(ReviewofSystem)
    examination = models.ManyToManyField(Examination)
    diagnosis = models.ManyToManyField(Diagnosis)
    investgation = models.ManyToManyField(Investgation)
    treatment = models.ManyToManyField(Treatment)
    medication = models.ManyToManyField(Medication)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    follow_up_date = models.DateField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient.firstname} - {self.patient.lastname}'
    

    def calculate_total_price(self):
        # Calculate total price based on selected categories, categories2, and categories3
        total_price = sum(category.price for category in self.treatment.all())
        total_price += sum(category.price for category in self.investgation.all())
        total_price += sum(category.price for category in self.medication.all())
        return total_price
    

    class Meta:
        verbose_name_plural = 'Medical History'


