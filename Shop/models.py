from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('snack', 'Snack'),
        ('biscuit', 'Biscuit'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    weight = models.CharField(max_length=20,  blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='snack')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_taken = models.BooleanField(default=False)
    status_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
