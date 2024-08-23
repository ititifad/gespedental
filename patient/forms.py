from django import forms
from .models import *
from django.forms import DateInput
from django.forms import inlineformset_factory
from django.forms.fields import DateField
from .widgets import *

class DateInput(DateInput):
    input_type = 'date'

class PatientRegistrationForm(forms.ModelForm):
    DOR = DateField(widget=DateInput)
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

    PERMANENT_DENTITION_CHOICES = [
        ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'),
        ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
        ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'),
        ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48')
    ]

    TEMPORARY_DENTITION_CHOICES = [
        ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'),
        ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'),
        ('71', '71'), ('72', '72'), ('73', '73'), ('74', '74'), ('75', '75'),
        ('81', '81'), ('82', '82'), ('83', '83'), ('84', '84'), ('85', '85')
    ]

    permanent_dentition = forms.MultipleChoiceField(
        choices=PERMANENT_DENTITION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permanent Dentition"
    )

    temporary_dentition = forms.MultipleChoiceField(
        choices=TEMPORARY_DENTITION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Temporary Dentition"
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
            'permanent_dentition', 
            'temporary_dentition',
            'medication_cash', 
            'medication_insurance', 
            'treatment_discount', 
            'investgation_discount', 
            'medication_discount', 
            'payment_type', 
            'follow_up_date', 
            'notes',
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


    