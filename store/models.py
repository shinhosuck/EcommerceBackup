from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db import models
from django.utils import timezone
from PIL import Image



class Customer(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return f"{self.customer}"


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    image = models.ImageField(default="productImages/defaultProductImage.jpg", upload_to="productImages")
    brand_image = models.ImageField(default="brandImages/defaultBrandImage.jpg", upload_to="brandImages")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    on_stock = models.BooleanField(default=True)
    times_ordered = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width > 400 or img.height > 400:
            new_img = (400, 400)
            img.thumbnail(new_img)
            img.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.brand_image.path)
        if img.width > 400 or img.height > 400:
            new_img = (400, 400)
            img.thumbnail(new_img)
            img.save(self.brand_image.path)

    def __str__(self):
        return self.product_name



class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_purchased = models.DateTimeField(default=timezone.now)
    open_basket = models.BooleanField(default=True)

    def __str__(self):
        return f"Product: {self.product}, Quantity: {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True)
    open_order = models.BooleanField(default=True)
    delivered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Customer: {self.customer}, Open: {self.open_order}, Delivered: {self.delivered}"
