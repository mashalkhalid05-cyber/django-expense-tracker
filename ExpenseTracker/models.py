from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    date=models.DateField()
    description=models.TextField(max_length=200,blank=True)

    def __str__(self):
        return str(self.amount)
        

class Budget(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount=models.IntegerField()
    year=models.IntegerField()
    month=models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"