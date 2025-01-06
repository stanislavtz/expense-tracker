from django.db import models

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
