from django.db import models
from django.contrib.auth.models import User 
from categories.models import Category

# Create your models here.
QUANTITY_CHOICES = (
    ('50grams','50GRAMS'),
    ('100grams', '100GRAMS'),
    ('1kg','1KG'),
    ('2kg','2KG'),
    ('3kg','3KG'),
)

class ProductRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='products')
    comment = models.TextField(blank=True)
    ratings = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return self.user.username


class Shops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    ratings = models.CharField(max_length=5, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="shops/",blank=True, null=True)

    def __str__(self):
        return self.user.username


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)
    price = models.PositiveIntegerField()
    offer_price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products_images/",blank=True)
    tag_name = models.CharField(max_length=150)
    quantity = models.CharField(max_length=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='category')
    products_description = models.TextField(blank=True, null=True)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, blank=True, null=True, related_name='shop')

    def __str__(self):
        return self.user.username


class OrderedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item= models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    quantity_in_grams = models.CharField(max_length=150, choices=QUANTITY_CHOICES,default='50grams',blank=True,null=True)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, blank=True, null=True, related_name='shops')

    def __str__(self):
        return self.user.username

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    product = models.ManyToManyField(Products)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    items = models.ManyToManyField(OrderedItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.CASCADE, blank=True, related_name='order_address', null=True)
    retailer_assigned = models.BooleanField(default=False,blank=True, null=True)
    amount = models.CharField(max_length=200, blank=True,null=True)
    payment_id = models.CharField(max_length=400, blank=True,null=True)
    payment_status = models.BooleanField(default=False, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, blank=True, null=True, related_name='order_shop')

    def __str__(self):
        return self.user.username

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='final_order')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    address1 = models.TextField()
    address2 = models.TextField()
    pincode = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.username

