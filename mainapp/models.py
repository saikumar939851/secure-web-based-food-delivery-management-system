from django.db import models


# -----------------------------
# USER MODEL (Admin / Restaurant / User)
# -----------------------------

class User(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('restaurant', 'Restaurant'),
        ('user', 'User'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -----------------------------
# CATEGORY MODEL
# -----------------------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# -----------------------------
# FOOD ITEM MODEL
# -----------------------------

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -----------------------------
# CART MODEL
# -----------------------------

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.food.name}"


# -----------------------------
# ORDER MODEL
# -----------------------------

class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, default='Unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# -----------------------------
# ORDER ITEM MODEL
# -----------------------------

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.food.name} (Order {self.order.id})"
# -----------------------------
# FEEDBACK MODEL
# -----------------------------

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_feedbacks')
    message = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} -> {self.restaurant.name}"
