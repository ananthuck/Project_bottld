from django.db import models

# Create your models here.

class Category(models.Model):
    productcategory = models.CharField(max_length=150)

class Product(models.Model):
    productname = models.CharField(max_length=100)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image = models.ImageField(upload_to="image/", null=True)

class Userlogin(models.Model):
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    otp_verified = models.BooleanField(default=False)

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

