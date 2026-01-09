"""Django models for the rev core app."""



from django.db import models


# Create your models here.

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.amount} on {self.date}"
    




class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, unique=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Userprofile(models.Model):
    profile=models.OneToOneField(User,on_delete=models.CASCADE)    