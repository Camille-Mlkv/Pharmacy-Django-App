from time import tzname
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from collections import defaultdict

from django.utils.timezone import get_current_timezone
import datetime
import calendar
from calendar import HTMLCalendar
import pytz

from django.db.models import Avg,Count,Sum,F
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from statistics import median, mode

from ..forms import  AdminSignUpForm,MedicationForm,PharmacyDepartmentForm,SupplierForm,MedicationSearchForm
from ..models import  User,Medication,PharmacyDepartment,Supplier,Sale,Employee,Customer
from ..decorators import admin_required

import os
from PharmacyApp import settings



class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admin_home')
    

def AdminHome(request):
    tz = get_current_timezone()
    stored_date = datetime.datetime.now()
    m=stored_date.month
    y=stored_date.year
    desired_date = stored_date + tz.utcoffset(stored_date)

    ttimezone = pytz.timezone("Europe/Minsk") 
    mydt = ttimezone.localize(desired_date) 
    #timezone_name=mydt.tzname()
    #timezone_name=desired_date.tzname()
    timezone_name=desired_date.astimezone().tzinfo
    cal=HTMLCalendar().formatmonth(y,m)
    return render(request, 'admins/admin_home.html',{'date':desired_date,'calendar':cal,'timezone':timezone_name})
    

@login_required
@admin_required
def add_medication(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home') 
    else:
        form = MedicationForm()
    return render(request, 'add_medication.html', {'form': form})



def view_medications(request):
    medications = Medication.objects.all()
    return render(request, 'view_medications.html', {'medications': medications})


@login_required
@admin_required
def edit_medication(request, medication_id):
    medication = get_object_or_404(Medication, id=medication_id)
    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('view_medications') 
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'edit_medication.html', {'form': form})


@login_required
@admin_required
def delete_medication(request, medication_id):
    medication = get_object_or_404(Medication, id=medication_id)
    if request.method == 'POST':
        medication.delete()
        return redirect('view_medications')
    

@login_required
@admin_required
def add_department(request):
    if request.method == 'POST':
        form = PharmacyDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = PharmacyDepartmentForm()
    return render(request, 'add_department.html', {'form': form})


@login_required
@admin_required
def view_departments(request):
    departments = PharmacyDepartment.objects.all()
    return render(request, 'view_departments.html', {'departments': departments})


@login_required
@admin_required
def edit_department(request, department_id):
    department = get_object_or_404(PharmacyDepartment, id=department_id)
    if request.method == 'POST':
        form = PharmacyDepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return redirect('view_departments') 
    else:
        form = PharmacyDepartmentForm(instance=department)
    return render(request, 'edit_department.html', {'form': form})


@login_required
@admin_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

@login_required
def view_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'view_suppliers.html', {'suppliers': suppliers})

@login_required
@admin_required
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('view_suppliers')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})


@login_required
@admin_required
def search_medication(request):
    if request.method == 'GET':
        form = MedicationSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            medications = Medication.objects.filter(name__icontains=query)
            return render(request, 'medication_search_results.html', {'medications': medications, 'query': query})
    return render(request, 'medication_search.html', {'form': MedicationSearchForm()})



# def view_sales(request):
#     sales = Sale.objects.all()
#     total_revenue = 0 
#     sales_by_pickup_point = defaultdict(list)
#     for sale in sales:
#         sales_by_pickup_point[sale.pickup_point].append(sale)
#         total_revenue += sale.product.cost * sale.quantity

#     return render(request, 'view_sales.html', {'sales_by_pickup_point': dict(sales_by_pickup_point), 'total_revenue': total_revenue})

@login_required
def view_sales(request):
    sales = Sale.objects.all()

    sales_by_pickup_point = defaultdict(list)
    for sale in sales:
        sales_by_pickup_point[sale.pickup_point].append(sale)

    revenue_by_pickup_point = defaultdict(float)

    for pickup_point, sales in sales_by_pickup_point.items():
        revenue = sum(sale.product.cost * sale.quantity for sale in sales)
        revenue_by_pickup_point[pickup_point] = revenue

    total_revenue = sum(revenue_by_pickup_point.values())

    return render(request, 'view_sales.html', {'sales_by_pickup_point': dict(sales_by_pickup_point), 'revenue_by_pickup_point': dict(revenue_by_pickup_point), 'total_revenue': total_revenue})


def view_employees(request):
    employees=Employee.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})


def filter_medications(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    medications = Medication.objects.all()

    if min_price:
        medications = medications.filter(cost__gte=min_price)
    if max_price:
        medications = medications.filter(cost__lte=max_price)

    return render(request, 'view_medications.html', {'medications': medications})

def calculate_statistics():
    sales = Sale.objects.all()
    if not sales:
        return None
    
    average_sales = sales.aggregate(avg_sales=Avg('quantity'))['avg_sales']
    
    amounts = [sale.quantity for sale in sales]
    median_sales = median(amounts)
    
    #mode_sales = mode(amounts)
    
    return {
        'average_sales': average_sales,
        'median_sales': median_sales,
        #'mode_sales': mode_sales,
    }

def calculate_age_statistics():
    clients = Customer.objects.all()
    if not clients:
        return None
    current_date = datetime.date.today()
    total_years = sum((current_date - client.birth_date).days // 365 for client in clients)
    average_age = total_years / len(clients)
    
    ages = [(current_date - client.birth_date).days // 365 for client in clients]
    median_age = median(ages)
    
    return {
        'average_age': round(average_age, 2),  # Округляем до двух знаков после запятой
        'median_age': median_age,
    }


def calculate_popular_product_type():
    product_types = Sale.objects.values('product__category').annotate(quantity=Count('id')).order_by('-quantity')
    if not product_types:
        return None
    if product_types:
        most_popular_type = product_types[0]['product__category']
    else:
        most_popular_type = None
    
    return most_popular_type


def get_sales_by_product_type():
    sales_by_product_type = Sale.objects.values('product__category').annotate(
        total_sales=Count('id')).order_by('-total_sales')
    
    return sales_by_product_type


def sales_distribution_chart():
    sales_data = get_sales_by_product_type()
    types = [sale['product__category'] for sale in sales_data]
    total_sales = [sale['total_sales'] for sale in sales_data]

    plt.figure(figsize=(8, 6))
    plt.pie(total_sales, labels=types, autopct='%1.1f%%')
    plt.title('Распределение продаж по типам товаров')
    plt.axis('equal') 
    save_path = os.path.join(settings.MEDIA_ROOT, 'sales_distribution_chart.png')
    plt.savefig(save_path)


def view_statistics(request):
    statistics = calculate_statistics()
    age_statistics = calculate_age_statistics()
    most_popular_type = calculate_popular_product_type()
    sales_distribution_chart()
    image_path = os.path.join(settings.MEDIA_URL, 'sales_distribution_chart.png')
    return render(request, 'view_statistics.html', {'statistics': statistics,'age_statistics': age_statistics,'popular':most_popular_type,'chart_image':image_path})