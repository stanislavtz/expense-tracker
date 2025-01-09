from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    created = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")

    def __str__(self):
        return self.name
