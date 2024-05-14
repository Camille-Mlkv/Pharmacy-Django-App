from django.shortcuts import render,redirect
#from .models import Contact,Article,Vacancy,Question,PromoCode,News
# Create your views here.
from ..models import Contact,Article,Vacancy,Question,PromoCode,News,FeedBack,Employee

def contacts(request):
    #contacts = Contact.objects.all()
    employees=Employee.objects.all()
    return render(request, 'contacts.html', {'employees': employees})

def about(request):
    return render(request, 'about.html')

def policy(request):
    return render(request, 'policy.html')

def vacancies(request):
    vacancies=Vacancy.objects.all()
    return render(request,'vacancies.html',{'vacancies':vacancies})

def index(request):
    latest_article = Article.objects.first()
    context = {
        'latest_article': latest_article
    }
    return render(request, 'index.html', context)

def questions(request):
    questions=Question.objects.all()
    return render(request,'questions.html',{'questions':questions})

def promocodes(request):
    active_promo_codes = PromoCode.objects.filter(is_active=True)
    archived_promo_codes = PromoCode.objects.filter(is_active=False)

    context = {
        'active_promo_codes': active_promo_codes,
        'archived_promo_codes': archived_promo_codes,
    }

    return render(request, 'promocodes.html', context)


def news(request):
    news = News.objects.all()
    return render(request, 'news.html', {'news': news})

def feedbacks(request):
    feedbacks=FeedBack.objects.all()
    return render(request,'feedbacks.html',{'feedbacks':feedbacks})