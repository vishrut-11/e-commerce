from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinLengthValidator
# Create your models here.

STATE_CHOICES=(
    ("andaman and nicobar islands", "andaman and nicobar islands"),
    ("andhra pradesh","andhra pradesh"),
    ("arunachal pradesh","arunachal pradesh"),
    ("assam","assam"),
    ("bihar","bihar"),
    ("chandigarh","chandigarh"),
    ("chhattisgarh","chhattisgarh"),
    ("dadra and nagar haveli","dadra and nagar haveli"),
    ("daman and diu dadra and nagar haveli","daman and diu dadra and nagar haveli"),
    ("goa","goa"),
    ("gujarat","gujarat"),
    ("haryana","haryana"),
    ("himachal pradesh","himachal pradesh"),
    ("jammu and kashmir","jammu and kashmir"),
    ("jharkhand","jharkhand"),
    ("karnataka","karnataka"),
    ("kerala ","kerala "),
    ("lakshadweep ","lakshadweep "),
    ("madhya pradesh","madhya pradesh"),
    ("maharashtra ","maharashtra "),
    ("manipur ","manipur "),
    ("meghalaya ","meghalaya "),
    ("mizoram ","mizoram"),
    ("nagaland ","nagaland "),
    ("odisha ","odisha"),
    ("puducherry ","puducherry "),
    ("punjab ","punjab "),
    ("rajasthan ","rajasthan "),
    ("sikkim ","sikkim "),
    ("tamil nadu ","tamil nadu "),
    ("telangana","telangana"),
    ("tripura","tripura"),
    ("uttarakhand","uttarakhand"),
    ("uttar pradesh","uttar pradesh"),
    ("west bengal","west bengal"),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ("M","Mobile"),
    ("L","Laptop"),
    ("TW","Top Wear"),
    ("BW","Bottom Wear"),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICES = (
    ("Accepted","Accepted"),
    ("Packed","Packed"),
    ("On The Way","On The Way"),
    ("Delivered","Delivered"),
    ("Cancel","Cancel"),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price