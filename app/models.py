from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Store the hashed password
    usertype = models.CharField(max_length=50)

    def set_password(self, password):
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        return check_password(password, self.password)

# User Model
class User(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

# Staff Model
class Staff(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Vendor Model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name


# User Model
class Services(models.Model):

    sname = models.CharField(max_length=255)
  
    description = models.TextField()

    def __str__(self):
        return self.sname
# Inventory Model
class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

# Package Model
class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

# Customer Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    estimate_price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Task Management for Staff
class Task(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status_choices = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    materials_used = models.ManyToManyField(Item, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

# Complaints Model
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Reviews Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Chat Model
class ChatMessage(models.Model):
    sender = models.ForeignKey(Login, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Login, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
class Sbook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    status=models.CharField(max_length=200)
 
class Assign_sbook(models.Model):
    sbook = models.ForeignKey(Sbook, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    adate = models.CharField(max_length=200)
  

