from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} [{self.price}원]'
    
    def get_absolute_url(self):
        return f'/final4/product/{self.pk}/'

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} [bought by {self.user.username}]'