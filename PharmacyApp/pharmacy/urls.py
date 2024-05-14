from django.urls import path,include,re_path
from pharmacy.views import views,customers,pharmacy,admins,employees

urlpatterns = [
    path('',pharmacy.home,name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('policy/',views.policy,name='policy'),
    path('vacancies/',views.vacancies,name='vacancies'),
    path('index/',views.index,name='index'),
    path('questions/',views.questions,name='questions'),
    path('promocodes/',views.promocodes,name='promocodes'),
    path('news/',views.news,name='news'),
    path('feedbacks/',views.feedbacks,name='feedbacks'),

    path('admin/home/', admins.AdminHome, name='admin_home'),

    path('add/medication', admins.add_medication, name='add_medication'),
    path('medications/', admins.view_medications, name='view_medications'),
    path('medications/<int:medication_id>/edit/', admins.edit_medication, name='edit_medication'),
    path('medications/<int:medication_id>/delete/', admins.delete_medication, name='delete_medication'),
    path('filter_medication',admins.filter_medications,name='filter_medications'),

    path('add/department', admins.add_department, name='add_department'),
    path('departments/', admins.view_departments, name='view_departments'),
    path('departments/<int:department_id>/edit/', admins.edit_department, name='edit_department'),

    path('add_supplier/', admins.add_supplier, name='add_supplier'),
    path('suppliers/', admins.view_suppliers, name='view_suppliers'),
    path('edit_supplier/<int:supplier_id>/edit/', admins.edit_supplier, name='edit_supplier'),
    #path(r'^supplier/(?P<supplier_id>\d+)$', admins.edit_supplier, name='edit_supplier'),

    path('search_medication/', admins.search_medication, name='search_medication'),

    path('view_sales/',admins.view_sales,name='view_sales'),

    path('view_employees/',admins.view_employees,name='view_employees'),

    path('customer/home/', customers.CustomerHome, name='customer_home'),

    path('pickup_points/', customers.view_pickup_points, name='view_pickup_points'),
    path('catalog/', customers.view_catalog, name='view_catalog'),
    path('buy_medication/<int:medication_id>/',customers.buy_medication,name='buy_medication'),
    path('customer/purchases/', customers.customer_purchases, name='customer_purchases'),
    path('leave_feedback/',customers.leave_feedback,name='leave_feedback'),
    path('get_age/',customers.get_age,name='get_age'),
    path('get_country/',customers.get_country,name='get_country'),

    path('employee/home',employees.EmployeeHome,name='employee_home'),
    path('admin/statistics',admins.view_statistics,name='view_statistics'),

]

