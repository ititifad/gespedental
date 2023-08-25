from django.shortcuts import render, redirect
from .models import Patient, MedicalHistory
from .forms import *
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate, TruncMonth, TruncYear  # Add this import
from django.contrib import messages
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.views import View
import calendar
from .filters import MedicalHistoryFilter
from weasyprint import HTML
import csv
from io import BytesIO


def is_valid_queryparam(param):
    return param != '' and param is not None


today = datetime.now().date()

def home(request):
    qs = Patient.objects.all()
    


    firstname_contains_query = request.GET.get('firstname_contains')

    lastname_contains_query = request.GET.get('lastname_contains')

    if is_valid_queryparam(firstname_contains_query):
        qs = qs.filter(firstname__icontains=firstname_contains_query)

    if is_valid_queryparam(lastname_contains_query):
        qs = qs.filter(lastname__icontains=lastname_contains_query)


    total_patients = qs.count()
    registered_today = qs.filter(created_at__date=today).count()
    attended_today = MedicalHistory.objects.filter(created_at__date=today).count()

    context = {
        'patients':qs,
        'total_patients':total_patients,
        'registered_today':registered_today,
        'attended_today':attended_today
    }

    return render(request, 'home.html', context)


def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, f'Patient has been Successfuly Added')

            return redirect('home')
        

    else:
        form = PatientRegistrationForm()
            

    return render(request, 'add_patient.html', {'form':form})


def Medication(request, pk):
    patient = Patient.objects.get(id=pk)
    form = MedicalHistoryForm(initial={'patient':patient})
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully Added Medical History for {patient}')
            return redirect('home')
    context = {'form':form, 'patient': patient}
    return render(request, 'medical_history_form.html', context)


def patient_detail(request, pk):
    patient = Patient.objects.get(id=pk)

    treatments = patient.patientmedicalhistory.all()
    
    context = {
        'patient': patient,
        'treatments':treatments
        }
    return render(request, 'patient_detail.html', context)


class AnalyticsView(View):
    def get(self, request, *args, **kwargs):
        # Patient Demographics
        gender_distribution = Patient.objects.values('gender').annotate(count=Count('id'))
        location_distribution = Patient.objects.values('address').annotate(count=Count('id'))

        # Treatment Analysis
        popular_treatments = MedicalHistory.objects.values('treatment__name').annotate(count=Count('id')).order_by('-count')[:5]
        total_revenue_by_treatment = MedicalHistory.objects.values('treatment__name').annotate(total_revenue=Sum('amount')).order_by('-total_revenue')

        # Payment Insights
        payment_type_distribution = MedicalHistory.objects.values('payment_type__name').annotate(count=Count('id'))
        revenue_by_payment_type = MedicalHistory.objects.values('payment_type__name').annotate(total_revenue=Sum('amount')).order_by('-total_revenue')

        # Patient Engagement
        patient_visits_over_time = MedicalHistory.objects.annotate(date=TruncDate('created_at')).values('date').annotate(visit_count=Count('id')).order_by('date')
        new_patient_acquisition_rate = Patient.objects.filter(created_at__gte=today).count() / Patient.objects.all().count() * 100

        # Revenue Trends
        monthly_revenue_trends = MedicalHistory.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_revenue=Sum('amount')).order_by('month')
        yearly_revenue_trends = MedicalHistory.objects.annotate(year=TruncYear('created_at')).values('year').annotate(total_revenue=Sum('amount')).order_by('year')
        revenue_by_treatment = MedicalHistory.objects.values('treatment__name').annotate(total_revenue=Sum('amount')).order_by('-total_revenue')

        # Medical History
        total_medical_history_entries = MedicalHistory.objects.count()
        top_patients_by_medical_history = Patient.objects.annotate(history_count=Count('patientmedicalhistory')).order_by('-history_count')[:5]

        context = {
            'gender_distribution': gender_distribution,
            'location_distribution': location_distribution,
            'popular_treatments': popular_treatments,
            'total_revenue_by_treatment': total_revenue_by_treatment,
            'payment_type_distribution': payment_type_distribution,
            'revenue_by_payment_type': revenue_by_payment_type,
            'patient_visits_over_time': patient_visits_over_time,
            'new_patient_acquisition_rate': new_patient_acquisition_rate,
            'monthly_revenue_trends': monthly_revenue_trends,
            'yearly_revenue_trends': yearly_revenue_trends,
            'revenue_by_treatment': revenue_by_treatment,
            'total_medical_history_entries': total_medical_history_entries,
            'top_patients_by_medical_history': top_patients_by_medical_history,
        }

        return render(request, 'analytics.html', context)
    

class RevenueByPaymentTypeView(View):
    def get(self, request, *args, **kwargs):
        # Get payment types
        payment_types = PaymentType.objects.all()

        # Calculate date ranges for each time interval
        today = datetime.now().date()
        last_week_start = today - timedelta(days=today.weekday() + 7)
        last_month_start = today.replace(day=1) - timedelta(days=1)
        last_year_start = today.replace(month=1, day=1) - timedelta(days=1)

        # Aggregate revenue data
        daily_revenue = self.aggregate_revenue(today, today)
        weekly_revenue = self.aggregate_revenue(last_week_start, today)
        monthly_revenue = self.aggregate_revenue(last_month_start, today)
        yearly_revenue = self.aggregate_revenue(last_year_start, today)

        context = {
            'payment_types': payment_types,
            'daily_revenue': daily_revenue,
            'weekly_revenue': weekly_revenue,
            'monthly_revenue': monthly_revenue,
            'yearly_revenue': yearly_revenue,
        }

        return render(request, 'revenue_by_payment_type.html', context)

    def aggregate_revenue(self, start_date, end_date):
        revenue_data = []
        payment_types = PaymentType.objects.all()
        for payment_type in payment_types:
            total_revenue = MedicalHistory.objects.filter(
                payment_type=payment_type,
                created_at__date__range=(start_date, end_date)
            ).aggregate(total_revenue=Sum('amount'))['total_revenue']
            if total_revenue is None:
                total_revenue = 0
            revenue_data.append({
                'payment_type': payment_type,
                'total_revenue': total_revenue,
            })
        return revenue_data
    

class FilteredMedicalHistoryView(View):
    template_name = 'filtered_medical_history.html'

    def get(self, request):
        filter = MedicalHistoryFilter(request.GET, queryset=MedicalHistory.objects.all())
        filtered_records = filter.qs

        context = {
            'filter': filter,
            'filtered_records': filtered_records,
        }
        return render(request, self.template_name, context)

class ExportFilteredMedicalHistoryView(View):
    def get(self, request):
        filter = MedicalHistoryFilter(request.GET, queryset=MedicalHistory.objects.all())
        filtered_records = filter.qs

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_medical_history.csv"'

        writer = csv.writer(response)
        writer.writerow(['Patient', 'Treatment', 'Amount', 'Payment Type', 'Date'])

        for record in filtered_records:
            writer.writerow([record.patient, record.treatment, record.amount, record.payment_type, record.created_at])

        return response

class ExportFilteredMedicalHistoryPDFView(View):
    def get(self, request):
        filter = MedicalHistoryFilter(request.GET, queryset=MedicalHistory.objects.all())
        filtered_records = filter.qs

        template_path = 'filtered_medical_history_pdf.html'
        context = {'filtered_records': filtered_records}

        html_template = render(request, template_path, context).content
        pdf_file = HTML(string=html_template).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="filtered_medical_history.pdf"'
        return response



def filter(request):
    qs = MedicalHistory.objects.all()
    treatments = Treatment.objects.all()
    payments_types = PaymentType.objects.all()
    firstname_contains_query = request.GET.get('firstname_contains')
    lastname_contains_query = request.GET.get('lastname_contains')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    treatment = request.GET.get('treatment')
    type = request.GET.get('payment_type')


    if is_valid_queryparam(firstname_contains_query):
        qs = qs.filter(firstname__icontains=firstname_contains_query)


    elif is_valid_queryparam(lastname_contains_query):
        qs = qs.filter(lastname__icontains=lastname_contains_query)


    if is_valid_queryparam(date_min):
        qs = qs.filter(created_at__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(created_at__lt=date_max)

    if is_valid_queryparam(treatment) and treatment != 'Choose...':
        qs = qs.filter(treatment__name=treatment)

    elif is_valid_queryparam(type) and type != 'Choose...':
        qs = qs.filter(type__name=type)



    context = {
        'queryset':qs,
        'treatments':treatments,
        'payments_types':payments_types
    }

    return render(request, 'filters.html', context)