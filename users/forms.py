from django import forms
from django.contrib.auth.forms import UserCreationForm
from patient.models import Doctor

class DoctorLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)