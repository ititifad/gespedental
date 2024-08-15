from django import forms
from .models import *
from django.forms import DateInput
from django.forms.fields import DateField

class DateInput(DateInput):
    input_type = 'date'

class PatientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'




class MedicalHistoryForm(forms.ModelForm):
    treatment_cash = forms.ModelMultipleChoiceField(
        queryset=Treatment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Treatment (Cash)"
    )
    treatment_insurance = forms.ModelMultipleChoiceField(
        queryset=Treatment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Treatment (Insurance)"
    )

    investgation_cash = forms.ModelMultipleChoiceField(
        queryset=Investgation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Investigation (Cash)"
    )
    investgation_insurance = forms.ModelMultipleChoiceField(
        queryset=Investgation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Investigation (Insurance)"
    )

    medication_cash = forms.ModelMultipleChoiceField(
        queryset=Medication.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Medication (Cash)"
    )
    medication_insurance = forms.ModelMultipleChoiceField(
        queryset=Medication.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Medication (Insurance)"
    )

    treatment_discount = forms.DecimalField(max_digits=5, decimal_places=2, required=False, initial=0.00, label="Treatment Discount (%)")
    investgation_discount = forms.DecimalField(max_digits=5, decimal_places=2, required=False, initial=0.00, label="Investigation Discount (%)")
    medication_discount = forms.DecimalField(max_digits=5, decimal_places=2, required=False, initial=0.00, label="Medication Discount (%)")

    review_of_systems = forms.ModelMultipleChoiceField(
        queryset=ReviewofSystem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Review of Systems"
    )

    examination = forms.ModelMultipleChoiceField(
        queryset=Examination.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Examination"
    )

    diagnosis = forms.ModelMultipleChoiceField(
        queryset=Diagnosis.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Diagnosis"
    )

    follow_up_date = DateField(widget=DateInput)
    class Meta:
        model = MedicalHistory
        fields = [
            'patient', 
            'history', 
            'review_of_systems', 
            'examination', 
            'diagnosis', 
            'treatment_cash', 
            'treatment_insurance', 
            'investgation_cash', 
            'investgation_insurance', 
            'medication_cash', 
            'medication_insurance', 
            'treatment_discount', 
            'investgation_discount', 
            'medication_discount', 
            'payment_type', 
            'follow_up_date', 
            'doctor'
        ]

    def __init__(self, *args, **kwargs):
        super(MedicalHistoryForm, self).__init__(*args, **kwargs)

        # Customize the label for cash price
        self.fields['treatment_cash'].queryset = Treatment.objects.all()
        self.fields['treatment_cash'].label_from_instance = lambda obj: f"{obj.name} - {obj.cash_price} TZS"

        self.fields['investgation_cash'].queryset = Investgation.objects.all()
        self.fields['investgation_cash'].label_from_instance = lambda obj: f"{obj.name} - {obj.cash_price} TZS"

        self.fields['medication_cash'].queryset = Medication.objects.all()
        self.fields['medication_cash'].label_from_instance = lambda obj: f"{obj.name} - {obj.cash_price} TZS"

        # Customize the label for insurance price
        self.fields['treatment_insurance'].queryset = Treatment.objects.all()
        self.fields['treatment_insurance'].label_from_instance = lambda obj: f"{obj.name} - {obj.insurance_price} TZS"

        self.fields['investgation_insurance'].queryset = Investgation.objects.all()
        self.fields['investgation_insurance'].label_from_instance = lambda obj: f"{obj.name} - {obj.insurance_price} TZS"

        self.fields['medication_insurance'].queryset = Medication.objects.all()
        self.fields['medication_insurance'].label_from_instance = lambda obj: f"{obj.name} - {obj.insurance_price} TZS"