from django.db import models

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
