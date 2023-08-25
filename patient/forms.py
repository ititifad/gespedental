from django import forms
from .models import *

class PatientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'


class MedicalHistoryForm(forms.ModelForm):

    class Meta:
        model = MedicalHistory
        fields = ('__all__')
   