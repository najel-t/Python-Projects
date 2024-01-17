from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    subtype = models.CharField(max_length=255, blank=True, null=True) 
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    pincode = models.CharField(max_length=10)
    address = models.TextField()
    order_date = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.fullname
    
class Cart(models.Model):
    uid = models.ForeignKey(User ,on_delete=models.CASCADE)
    pid = models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0.0)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    order_date = models.DateTimeField(default=timezone.now)
    order_number = models.CharField(max_length=10, unique=True, default='')

    def __str__(self):
        return f"Order #{self.order_number} for {self.user.username} on {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return self.text