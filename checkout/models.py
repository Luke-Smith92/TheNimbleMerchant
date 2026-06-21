from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=254)
    town_or_city = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_profile = models.ForeignKey(
    User,
    null=True,
    blank=True,
    on_delete=models.SET_NULL
)

    def __str__(self):
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"