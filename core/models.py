"""Django models for the rev core app."""



from django.db import models


# Create your models here.


class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.amount} on {self.date}"