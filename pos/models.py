from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    available_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', '-date_created',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Product: {self.name[:10]}>'
    

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)
    
    def __repr__(self):
        return f'<Purchase: GH{self.total_amount} by {self.username}>'

    def save(self, *args, **kwargs):
        self.product.available_quantity -= self.quantity
        self.price = self.price * int(self.quantity)
        self.product.save()
        super(Purchase, self).save(*args, **kwargs)

class Supply(models.Model):
    product = models.ForeignKey(Product, related_name="supplies", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    
    def __repr__(self):
        return f'<Supply: {self.product.name} {self.quantity}>'
    
    def save(self, *args, **kwargs):
        self.product.available_quantity = int(self.product.available_quantity) + int(self.quantity)
        self.product.save()
        super(Supply, self).save(*args, **kwargs)

class Expense(models.Model):
    description = models.CharField(max_length=600)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.description