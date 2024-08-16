from django import forms
import django_filters
from .models import MedicalHistory, Treatment, PaymentType, ReviewofSystem, Investgation

class MedicalHistoryFilter(django_filters.FilterSet):
    patient = django_filters.CharFilter(field_name='patient__firstname', lookup_expr='icontains')
    investgation = django_filters.ModelChoiceFilter(field_name='investgation', queryset=Investgation.objects.all())
    treatment = django_filters.ModelChoiceFilter(field_name='treatment', queryset=Treatment.objects.all())
    payment_type = django_filters.ModelChoiceFilter(field_name='payment_type', queryset=PaymentType.objects.all())
    review_of_systems = django_filters.ModelChoiceFilter(field_name='review_of_systems', queryset=ReviewofSystem.objects.all())
    # min_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    # max_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Greater or Less Than Date',
        widget=forms.TextInput(attrs={'type': 'date'}),
    )
    max_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Less Than or Equal Date',
        widget=forms.TextInput(attrs={'type': 'date'}),
    )



    class Meta:
        model = MedicalHistory
        fields = []

class MedicalFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Created at is greater than or equal to',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    created_at__lte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Created at is less than or equal to',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    class Meta:
        model = MedicalHistory
        fields = {
            'patient': ['exact'],
            'review_of_systems': ['exact'],
            'examination': ['exact'],
            'diagnosis': ['exact'],
            'investgation': ['exact'],
            'treatment': ['exact'],
            'medication': ['exact'],
            'payment_type': ['exact'],
            'doctor': ['exact'],
            'created_at': ['exact', 'date__gt', 'date__lt'],
        }