"""PharmacyApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from pharmacy.views import pharmacy,customers,employees,admins

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pharmacy.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', pharmacy.SignUpView.as_view(), name='signup'),
    path('accounts/signup/customer/', customers.CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/signup/employee/', employees.EmployeeSignUpView.as_view(), name='employee_signup'),
    path('accounts/signup/admin/', admins.AdminSignUpView.as_view(), name='admin_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)