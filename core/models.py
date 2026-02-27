"""Django models for the rev core app."""



from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    user_name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100,blank= False, null=False)
    def clean(self):
        if not self.password:
            raise ValidationError("Password cannot be empty.")
        if len(self.password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")



    



class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Education', 'Education'),
        ('Health', 'Health'),
        ('Shopping', 'Shopping'),
        ('Travel', 'Travel'),
        ('Personal Care', 'Personal Care'),
        ('bill', 'bill'),
        
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    amount = models.FloatField(max_length=False,blank=False, null=False)
    date = models.DateField( auto_now_add=True) 

    def __str__(self):
        return f"{self.title} - {self.amount} on {self.date}"
    






class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(User, on_delete=models.CASCADE)