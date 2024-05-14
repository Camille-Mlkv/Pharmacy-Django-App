from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

import requests
from django.http import JsonResponse

# from ..decorators import student_required
from ..forms import  CustomerSignUpForm,PurchaseForm,FeedbackForm
from ..models import Customer, User,PickupPoint,Medication,Purchase,Sale
from ..decorators import customer_required


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer_home')
    

def CustomerHome(request):
    return render(request, 'customers/customer_home.html')


def view_pickup_points(request):
    points = PickupPoint.objects.all()
    return render(request, 'view_pickup_points.html', {'points': points})


def view_catalog(request):
    medications = Medication.objects.all()
    return render(request, 'view_medications.html', {'medications': medications})


@login_required
@customer_required
def buy_medication(request, medication_id):
    medication = get_object_or_404(Medication, pk=medication_id)
    customer = request.user.customer
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            pickup_point = form.cleaned_data['pickup_point']
            quantity = form.cleaned_data['quantity']
            product=medication
            date_sold=datetime.now()
            purchase = Purchase.objects.create(buyer=request.user, product=product,pickup_point=pickup_point, quantity=quantity,date_sold=date_sold)
            #check if this sale already exists
            existing_sale=Sale.objects.filter(product=medication,pickup_point=pickup_point)
            if existing_sale:
                old_quantity = Sale.objects.get(product=medication,pickup_point=pickup_point).quantity
                new_quantity=old_quantity+quantity;
                Sale.objects.filter(product=medication,pickup_point=pickup_point).update(quantity=new_quantity)
            else:
                sale=Sale.objects.create(product=product,quantity=quantity,pickup_point=pickup_point)#pickup_point=pickup_point
            return redirect('customer_home') 
    else:
        form = PurchaseForm()
    return render(request, 'buy_medication.html', {'form': form, 'medication': medication})

    


@login_required
@customer_required
def customer_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'customer_purchases.html', {'purchases': purchases})
        

@login_required
@customer_required
def leave_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.date = datetime.now()
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('customer_home')
    else:
        form = FeedbackForm()
    return render(request, 'leave_feedback.html', {'form': form})



def get_age(request):
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET['name']
        response = requests.get(f"https://api.agify.io?name={name}")
        data = response.json()
        age = data.get('age')
        name = data.get('name')
        return render(request, 'get_age.html', {'age': age, 'name': name})
        #return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})


def get_country(request):
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET['name']
        response = requests.get(f"https://api.nationalize.io/?name={name}")
        data = response.json()
        name = data.get('name')
        countries = data.get('country')
        return render(request, 'get_country.html', {'countries': countries,'name':name})
    return JsonResponse({'error': 'Invalid request'})