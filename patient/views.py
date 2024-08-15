import os
from django.shortcuts import render, redirect
from .models import Patient, MedicalHistory
from .forms import *
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate, TruncMonth, TruncYear  # Add this import
from .utils import render_to_pdf
from django.conf import settings
from django.template.loader import get_template
from django.contrib import messages
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.views import View
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import io
import calendar
from .filters import MedicalHistoryFilter, MedicalFilter
from django.contrib.auth.decorators import login_required
import csv
from io import BytesIO



def is_valid_queryparam(param):
    return param != '' and param is not None


today = datetime.now().date()

@login_required
def medical_history(request):
    qs = MedicalHistory.objects.order_by('-id')
    firstname_contains_query = request.GET.get('firstname_contains')

    lastname_contains_query = request.GET.get('lastname_contains')

    if is_valid_queryparam(firstname_contains_query):
        qs = qs.filter(patient__firstname__icontains=firstname_contains_query)

    if is_valid_queryparam(lastname_contains_query):
        qs = qs.filter(patient__lastname__icontains=lastname_contains_query)

    context = {
        'history':qs
    }

    return render(request, 'medical_history.html', context)

@login_required
def home(request):
    qs = Patient.objects.order_by('-id')
    


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

@login_required
def Medication(request, pk):
    patient = Patient.objects.get(id=pk)
    form = MedicalHistoryForm(initial={'patient': patient})

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.save()

            # Save the many-to-many relationships
            form.save_m2m()

            # Retrieve discounts from the form
            treatment_discount = form.cleaned_data.get('treatment_discount', 0)
            investgation_discount = form.cleaned_data.get('investgation_discount', 0)
            medication_discount = form.cleaned_data.get('medication_discount', 0)

            # Handling treatment with discount
            for treatment in form.cleaned_data.get('treatment_cash', []):
                discounted_price = treatment.cash_price * (1 - (treatment_discount / 100))
                # Log or process the discounted price if necessary
                medical_history.treatment.add(treatment)
                # You can print/log discounted_price for debugging
                print(f"Discounted cash treatment price: {discounted_price}")

            for treatment in form.cleaned_data.get('treatment_insurance', []):
                discounted_price = treatment.insurance_price * (1 - (treatment_discount / 100))
                medical_history.treatment.add(treatment)
                print(f"Discounted insurance treatment price: {discounted_price}")

            # Handling investigation with discount
            for investgation in form.cleaned_data.get('investgation_cash', []):
                discounted_price = investgation.cash_price * (1 - (investgation_discount / 100))
                medical_history.investgation.add(investgation)
                print(f"Discounted cash investigation price: {discounted_price}")

            for investgation in form.cleaned_data.get('investgation_insurance', []):
                discounted_price = investgation.insurance_price * (1 - (investgation_discount / 100))
                medical_history.investgation.add(investgation)
                print(f"Discounted insurance investigation price: {discounted_price}")

            # Handling medication with discount
            for medication in form.cleaned_data.get('medication_cash', []):
                discounted_price = medication.cash_price * (1 - (medication_discount / 100))
                medical_history.medication.add(medication)
                print(f"Discounted cash medication price: {discounted_price}")

            for medication in form.cleaned_data.get('medication_insurance', []):
                discounted_price = medication.insurance_price * (1 - (medication_discount / 100))
                medical_history.medication.add(medication)
                print(f"Discounted insurance medication price: {discounted_price}")

            messages.success(request, f'Successfully Added Medical History for {patient.firstname} {patient.lastname}')
            return redirect('home')

    context = {'form': form, 'patient': patient}
    return render(request, 'medical_history_form.html', context)



@login_required
def patient_detail(request, pk):
    patient = Patient.objects.get(id=pk)

    treatments = patient.patientmedicalhistory.all().order_by('-id')
    
    context = {
        'patient': patient,
        'treatments':treatments
        }
    return render(request, 'patient_detail.html', context)


# class AnalyticsView(View):
#     def get(self, request, *args, **kwargs):
#         # Patient Demographics
#         gender_distribution = Patient.objects.values('gender').annotate(count=Count('id'))
#         location_distribution = Patient.objects.values('address').annotate(count=Count('id'))

#         # Treatment Analysis
#         popular_treatments = MedicalHistory.objects.values('treatment__name').annotate(count=Count('id')).order_by('-count')[:5]
#         total_revenue_by_treatment = MedicalHistory.objects.values('treatment__name').annotate(total_revenue=Sum('amount')).order_by('-total_revenue')

#         # Payment Insights
#         payment_type_distribution = MedicalHistory.objects.values('payment_type__name').annotate(count=Count('id'))
#         revenue_by_payment_type = MedicalHistory.objects.values('payment_type__name').annotate(total_revenue=Sum('amount')).order_by('-total_revenue')

#         # Patient Engagement
#         patient_visits_over_time = MedicalHistory.objects.annotate(date=TruncDate('created_at')).values('date').annotate(visit_count=Count('id')).order_by('date')
#         new_patient_acquisition_rate = Patient.objects.filter(created_at__gte=today).count() / Patient.objects.all().count() * 100

#         # Revenue Trends
#         monthly_revenue_trends = MedicalHistory.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_revenue=Sum('amount')).order_by('month')
#         yearly_revenue_trends = MedicalHistory.objects.annotate(year=TruncYear('created_at')).values('year').annotate(total_revenue=Sum('amount')).order_by('year')
#         revenue_by_treatment = MedicalHistory.objects.values('treatment__name').annotate(total_revenue=Sum('amount')).order_by('-total_revenue')

#         # Medical History
#         total_medical_history_entries = MedicalHistory.objects.count()
#         top_patients_by_medical_history = Patient.objects.annotate(history_count=Count('patientmedicalhistory')).order_by('-history_count')[:5]

#         context = {
#             'gender_distribution': gender_distribution,
#             'location_distribution': location_distribution,
#             'popular_treatments': popular_treatments,
#             'total_revenue_by_treatment': total_revenue_by_treatment,
#             'payment_type_distribution': payment_type_distribution,
#             'revenue_by_payment_type': revenue_by_payment_type,
#             'patient_visits_over_time': patient_visits_over_time,
#             'new_patient_acquisition_rate': new_patient_acquisition_rate,
#             'monthly_revenue_trends': monthly_revenue_trends,
#             'yearly_revenue_trends': yearly_revenue_trends,
#             'revenue_by_treatment': revenue_by_treatment,
#             'total_medical_history_entries': total_medical_history_entries,
#             'top_patients_by_medical_history': top_patients_by_medical_history,
#         }

#         return render(request, 'analytics.html', context)

class AnalyticsView(View):
    def get(self, request, *args, **kwargs):
        # Patient Demographics
        gender_distribution = Patient.objects.values('gender').annotate(count=Count('id'))
        location_distribution = Patient.objects.values('address').annotate(count=Count('id'))

        # Treatment Analysis
        popular_treatments = MedicalHistory.objects.values('treatment__name').annotate(count=Count('id')).order_by('-count')[:5]
        total_revenue_by_treatment = MedicalHistory.objects.values('treatment__name').annotate(total_revenue=Sum('treatment__cash_price')).order_by('-total_revenue')

        # Payment Insights
        payment_type_distribution = MedicalHistory.objects.values('payment_type__name').annotate(count=Count('id'))
        revenue_by_payment_type = MedicalHistory.objects.values('payment_type__name').annotate(total_revenue=Sum('treatment__cash_price')).order_by('-total_revenue')

        # Patient Engagement
        patient_visits_over_time = MedicalHistory.objects.annotate(date=TruncDate('created_at')).values('date').annotate(visit_count=Count('id')).order_by('date')
        today = datetime.now().date()
        new_patient_acquisition_rate = Patient.objects.filter(created_at__date=today).count() / Patient.objects.all().count() * 100

        # Revenue Trends
        monthly_revenue_trends = MedicalHistory.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_revenue=Sum('treatment__cash_price')).order_by('month')
        yearly_revenue_trends = MedicalHistory.objects.annotate(year=TruncYear('created_at')).values('year').annotate(total_revenue=Sum('treatment__cash_price')).order_by('year')
        revenue_by_treatment = MedicalHistory.objects.values('treatment__name').annotate(total_revenue=Sum('treatment__cash_price')).order_by('-total_revenue')

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
    

# class RevenueByPaymentTypeView(View):
#     def get(self, request, *args, **kwargs):
#         # Get payment types
#         payment_types = PaymentType.objects.all()

#         # Calculate date ranges for each time interval
#         today = datetime.now().date()
#         last_week_start = today - timedelta(days=today.weekday() + 7)
#         last_month_start = today.replace(day=1) - timedelta(days=1)
#         last_year_start = today.replace(month=1, day=1) - timedelta(days=1)

#         # Aggregate revenue data
#         daily_revenue = self.aggregate_revenue(today, today)
#         weekly_revenue = self.aggregate_revenue(last_week_start, today)
#         monthly_revenue = self.aggregate_revenue(last_month_start, today)
#         yearly_revenue = self.aggregate_revenue(last_year_start, today)

#         context = {
#             'payment_types': payment_types,
#             'daily_revenue': daily_revenue,
#             'weekly_revenue': weekly_revenue,
#             'monthly_revenue': monthly_revenue,
#             'yearly_revenue': yearly_revenue,
#         }

#         return render(request, 'revenue_by_payment_type.html', context)

#     def aggregate_revenue(self, start_date, end_date):
#         revenue_data = []
#         payment_types = PaymentType.objects.all()
        
#         for payment_type in payment_types:
#             total_revenue = MedicalHistory.objects.filter(
#                 payment_type=payment_type,
#                 created_at__date__range=(start_date, end_date)
#             ).aggregate(total_revenue=Sum('calculate_total_price'))['total_revenue']
#             if total_revenue is None:
#                 total_revenue = 0
#             revenue_data.append({
#                 'payment_type': payment_type,
#                 'total_revenue': total_revenue,
#             })
#         return revenue_data

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
            total_revenue = 0

            medical_histories = MedicalHistory.objects.filter(
                payment_type=payment_type,
                created_at__date__range=(start_date, end_date)
            )

            for history in medical_histories:
                total_revenue += history.calculate_total_price()

            revenue_data.append({
                'payment_type': payment_type,
                'total_revenue': total_revenue,
            })

        return revenue_data
    

class FilteredMedicalHistoryView(View):
    template_name = 'filtered_medical_history.html'

    def get(self, request):
        # Initialize the filter with GET data
        filter = MedicalHistoryFilter(request.GET, queryset=MedicalHistory.objects.order_by('-id'))

        # Get the filtered records
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
            writer.writerow([record.patient, record.treatment, record.calculate_total_price(), record.payment_type, record.created_at])

        return response

class ExportFilteredMedicalHistoryPDFView(View):
    def get(self, request):
        filter = MedicalHistoryFilter(request.GET, queryset=MedicalHistory.objects.all())
        filtered_records = filter.qs

        template = 'filtered_medical_history_pdf.html'
        context = {'filtered_records': filtered_records}
        html = render_to_string(template, context)

        pdf_file = io.BytesIO()

        pisa.CreatePDF(html, dest=pdf_file)

        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="filtered_medical_history.pdf"'
  
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


# class AnalyticsByDoctorView(View):
#     def get(self, request, *args, **kwargs):
#         doctors = Doctor.objects.all()

#         # Calculate date ranges for each time interval
#         today = datetime.now().date()
#         last_week_start = today - timedelta(days=today.weekday() + 7)
#         last_month_start = today.replace(day=1) - timedelta(days=1)
#         last_year_start = today.replace(month=1, day=1) - timedelta(days=1)

#         doctor_revenue_data = []
        
#         for doctor in doctors:
#             daily_revenue = self.aggregate_revenue(doctor, today, today)
#             weekly_revenue = self.aggregate_revenue(doctor, last_week_start, today)
#             monthly_revenue = self.aggregate_revenue(doctor, last_month_start, today)
#             yearly_revenue = self.aggregate_revenue(doctor, last_year_start, today)

#             doctor_revenue_data.append({
#                 'doctor': doctor,
#                 'daily_revenue': daily_revenue,
#                 'weekly_revenue': weekly_revenue,
#                 'monthly_revenue': monthly_revenue,
#                 'yearly_revenue': yearly_revenue,
#             })

#         context = {
#             'doctor_revenue_data': doctor_revenue_data,
#         }

#         return render(request, 'analytics_by_doctor.html', context)

#     def aggregate_revenue(self, doctor, start_date, end_date):
#         revenue_data = []
#         payment_types = doctor.medicalhistory_set.values('payment_type__name').annotate(count=Count('id'))

#         for payment_type in payment_types:
#             total_revenue = doctor.medicalhistory_set.filter(
#                 payment_type__name=payment_type['payment_type__name'],
#                 created_at__date__range=(start_date, end_date)
#             ).aggregate(total_revenue=Sum('treatment__price'))['total_revenue']
#             if total_revenue is None:
#                 total_revenue = 0
#             revenue_data.append({
#                 'payment_type': payment_type['payment_type__name'],
#                 'total_revenue': total_revenue,
#             })
#         return revenue_data

# class AnalyticsByDoctorView(View):
#     def get(self, request, *args, **kwargs):
#         doctors = Doctor.objects.all()

#         # Calculate date ranges for each time interval
#         today = datetime.now().date()
#         last_week_start = today - timedelta(days=today.weekday() + 7)
#         last_month_start = today.replace(day=1) - timedelta(days=1)
#         last_year_start = today.replace(month=1, day=1) - timedelta(days=1)

#         doctor_revenue_data = []
#         total_revenue = 0
        
#         for doctor in doctors:
#             daily_revenue = self.aggregate_revenue(doctor, today, today)
#             weekly_revenue = self.aggregate_revenue(doctor, last_week_start, today)
#             monthly_revenue = self.aggregate_revenue(doctor, last_month_start, today)
#             yearly_revenue = self.aggregate_revenue(doctor, last_year_start, today)

#             doctor_revenue_data.append({
#                 'doctor': doctor,
#                 'daily_revenue': daily_revenue,
#                 'weekly_revenue': weekly_revenue,
#                 'monthly_revenue': monthly_revenue,
#                 'yearly_revenue': yearly_revenue,
#             })
            
#             total_revenue += (
#                 sum(entry['total_revenue'] for entry in daily_revenue) +
#                 sum(entry['total_revenue'] for entry in weekly_revenue) +
#                 sum(entry['total_revenue'] for entry in monthly_revenue) +
#                 sum(entry['total_revenue'] for entry in yearly_revenue)
#             )

#         context = {
#             'doctor_revenue_data': doctor_revenue_data,
#             'total_revenue': total_revenue,
#         }

#         return render(request, 'analytics_by_doctor.html', context)

#     def aggregate_revenue(self, doctor, start_date, end_date):
#         revenue_data = []
#         payment_types = doctor.medicalhistory_set.values('payment_type__name').annotate(count=Count('id'))

#         for payment_type in payment_types:
#             total_revenue = 0
#             medical_histories = doctor.medicalhistory_set.filter(
#                 payment_type__name=payment_type['payment_type__name'],
#                 created_at__date__range=(start_date, end_date)
#             )
#             for history in medical_histories:
#                 total_revenue += history.calculate_total_price()
                
#             revenue_data.append({
#                 'payment_type': payment_type['payment_type__name'],
#                 'total_revenue': total_revenue,
#             })
#         return revenue_data

class AnalyticsByDoctorView(View):
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()

        # Calculate date ranges for each time interval
        today = datetime.now().date()
        last_week_start = today - timedelta(days=today.weekday() + 7)
        last_month_start = today.replace(day=1) - timedelta(days=1)
        last_year_start = today.replace(month=1, day=1) - timedelta(days=1)

        doctor_revenue_data = []
        
        for doctor in doctors:
            daily_revenue = self.aggregate_revenue(doctor, today, today)
            weekly_revenue = self.aggregate_revenue(doctor, last_week_start, today)
            monthly_revenue = self.aggregate_revenue(doctor, last_month_start, today)
            yearly_revenue = self.aggregate_revenue(doctor, last_year_start, today)
            total_revenue = self.calculate_total_revenue(doctor, today, today)

            doctor_revenue_data.append({
                'doctor': doctor,
                'daily_revenue': daily_revenue,
                'weekly_revenue': weekly_revenue,
                'monthly_revenue': monthly_revenue,
                'yearly_revenue': yearly_revenue,
                'total_revenue': total_revenue,
            })

        context = {
            'doctor_revenue_data': doctor_revenue_data,
        }

        return render(request, 'analytics_by_doctor.html', context)

    def aggregate_revenue(self, doctor, start_date, end_date):
        revenue_data = []
        payment_types = doctor.medicalhistory_set.values('payment_type__name').annotate(count=Count('id'))

        for payment_type in payment_types:
            total_revenue = 0
            medical_histories = doctor.medicalhistory_set.filter(
                payment_type__name=payment_type['payment_type__name'],
                created_at__date__range=(start_date, end_date)
            )
            for history in medical_histories:
                total_revenue += history.calculate_total_price()
                
            revenue_data.append({
                'payment_type': payment_type['payment_type__name'],
                'total_revenue': total_revenue,
            })
        return revenue_data

    def calculate_total_revenue(self, doctor, start_date, end_date):
        total_revenue = 0
        medical_histories = doctor.medicalhistory_set.filter(
            created_at__date__range=(start_date, end_date)
        )
        for history in medical_histories:
            total_revenue += history.calculate_total_price()
        return total_revenue
    

# def generate_invoice_pdf(request, history_id):
#     history = MedicalHistory.objects.get(id=history_id)

#     # Get template HTML
#     template = get_template('invoice.html')
#     context = {'history': history}
#     html = template.render(context)

#     # Create a PDF file
#     pdf_file = HTML(string=html).write_pdf()

#     # Generate a response
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{history.id}.pdf"'
#     return response

# @login_required
# def generate_invoice_pdf(request, history_id):
#     history = MedicalHistory.objects.get(id=history_id)

#     # image_url = 'https://i.imgur.com/INCX0Dm.jpeg'

#     template = get_template('invoice.html')
    
#     context = {
#         'history':history,
#         'STATIC_ROOT': settings.STATIC_ROOT,
#         # 'image_url': image_url
#     }
#     html = template.render(context)
#     pdf = render_to_pdf('invoice.html', context)
#     return HttpResponse(pdf, content_type='application/pdf')

def generate_invoice_pdf(request, history_id):
    history = MedicalHistory.objects.get(id=history_id)

    # Get template HTML
    template = get_template('invoice.html')
    context = {'history': history}
    html = template.render(context)

    # Create a PDF file
    pdf_file = io.BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)

    # Generate a response
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{history.id}.pdf"'
    return response


class UpcomingFollowUpView(View):
    def get(self, request, *args, **kwargs):
        # Calculate the date for tomorrow
        tomorrow = datetime.now().date() + timedelta(days=1)
        
        # Retrieve all medical history records with upcoming follow-up date
        upcoming_follow_ups = MedicalHistory.objects.filter(follow_up_date=tomorrow)
        
        context = {
            'upcoming_follow_ups': upcoming_follow_ups,
            'upcoming_follow_up_count': upcoming_follow_ups.count()
        }
        
        return render(request, 'upcoming_follow_ups.html', context)
    

class MedicalHistoryReportView(View):
    template_name = 'medical_history_report.html'

    def get(self, request):
        # Initialize the filter with GET data
        filter = MedicalHistoryFilter(request.GET, queryset=MedicalHistory.objects.all())

        # Get the filtered records
        filtered_records = filter.qs

        context = {
            'filter': filter,
            'filtered_records': filtered_records,
        }

        return render(request, self.template_name, context)