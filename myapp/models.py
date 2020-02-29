from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator



class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=10, default='Windsor')

    def __str__(self):
        return self.name + ", " + self.warehouse


class Product(models.Model):
    Category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    available = models.BooleanField(default=True)
    interested = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def refill(self):
        stock = self.stock + 50
        if(stock >= 0):
            if(stock <= 1000):
                t = Product.objects.get(id=self.id)
                t.stock = stock
                t.save()
                return 1
            else:
                return 0
        else:
            return 0


    def getCategory(self):
        return self.Category.name


class Client(User):
    PROVINCE_CHOICES = [
         ('AB', 'Alberta'),
         ('MB', 'Manitoba'),
         ('ON', 'Ontario'),
         ('QC', 'Quebec'),
    ]
    company = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    Interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def interested_in(self):
        list = []
        interested = Client.objects.filter(username=self.username).values("Interested_in__name")
        for a in interested:
            list.append(a['Interested_in__name'])
        return list


class Order(models.Model):
    INT_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')
    ]
    Product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    Client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=0)
    order_status = models.PositiveIntegerField(choices=INT_CHOICES, default=1)
    status_date = models.DateField(default='2019-05-01')

    def __str__(self):
        return 'Order#' + str(self.id) + ': For ' + ' ' + self.Product.name + " by " + str(self.Client)

    def total_cost(self):
        return self.Product.price * self.num_unit
