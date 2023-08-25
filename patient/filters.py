import django_filters
from .models import MedicalHistory, Treatment, PaymentType

class MedicalHistoryFilter(django_filters.FilterSet):
    patient = django_filters.CharFilter(field_name='patient__firstname', lookup_expr='icontains')
    treatment = django_filters.ModelChoiceFilter(field_name='treatment', queryset=Treatment.objects.all())
    payment_type = django_filters.ModelChoiceFilter(field_name='payment_type', queryset=PaymentType.objects.all())
    min_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = MedicalHistory
        fields = []
