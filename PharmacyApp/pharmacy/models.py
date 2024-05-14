from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Contact(models.Model):
    employee_name = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    photo = models.ImageField(default='contact_photos/default_photo.png',upload_to='contact_photos/',blank=True)

    def __str__(self):
        return self.employee_name
    

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return self.title
    


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    requirements = models.TextField()
    job_type = models.CharField(max_length=50, choices=[
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ])

    def __str__(self):
        return self.title
    


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    


class PromoCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-date_created']


class News(models.Model):
    title = models.CharField(max_length=100)
    short_description=models.TextField()
    description = models.TextField()
    photo = models.ImageField(default='contact_photos/default_photo.png',upload_to='news_photo/',blank=True)

    def __str__(self):
        return self.title
    


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)



class PickupPoint(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    photo = models.ImageField(default='default_photo.png',upload_to='pickup_points_photo/')

    def __str__(self):
        return self.name
    

class Medication(models.Model):
    code = models.CharField(max_length=100)
    category=models.CharField(max_length=255,default='Adults')
    name = models.CharField(max_length=255)
    description = models.TextField()
    instruction=models.TextField(default='1 per day')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(default='default_photo.png',upload_to='medications_photo/')

    def __str__(self):
        return f"{self.name} {self.code} ({self.cost} рублей)"


class Purchase(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(Medication, on_delete=models.CASCADE)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  
    date_sold = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return f"{self.buyer.username}'s purchase of {self.product.name}"
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name = 'customer',related_query_name='customer')
    purchases = models.ManyToManyField(Purchase) #new
    phone_number = models.CharField(max_length=18,default='+375-25-111-11-11')
    birth_date = models.DateField(default='2000-01-01')
    def __str__(self):
        return self.user.username
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=18,default='+375-25-111-11-11')
    birth_date = models.DateField(default='2000-01-01')
    photo=models.ImageField(default='contact_photos/default_photo.png',upload_to='contact_photos/')
    def __str__(self):
        return self.user.username
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=18,default='+375-25-111-11-11')
    birth_date = models.DateField(default='2000-01-01')
    def __str__(self):
        return self.user.username


class PharmacyDepartment(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    number_of_employees = models.IntegerField(default=0)
    photo = models.ImageField(default='default_photo.png',upload_to='departments_photo/')
    def __str__(self):
        return self.name
    

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
class Sale(models.Model):
    product = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)  
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE)


class FeedBack(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    note = models.PositiveIntegerField()
    text = models.TextField()
    date = models.DateTimeField()
