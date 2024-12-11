from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Food(models.Model):
    foodname = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    available = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.foodname

class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Food, on_delete=models.CASCADE, db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    customer_name = models.ForeignKey(User, on_delete=models.PROTECT)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=400)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.BooleanField()
    datetime = models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return self.amount
    
class OrderItem(models.Model):
    STATUS_CHOICE = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure')
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ForeignKey(Food, on_delete=models.CASCADE)
    orderdate = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='PENDING')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"


