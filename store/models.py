from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#tip user lowercase classname_set to access that class objects eg OrderItem lass - orderitem_set.all()

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class MainCategory(models.Model):
    main_category = models.CharField(max_length=200, default="unknown")

    def __str__(self):
        return self.main_category

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=True)
    sub_category=models.CharField(max_length=200,default="others")

    def __str__(self):
        return self.sub_category

class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=False)
    image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url='/media/placeholder.png'
        return url


class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,default="incomplete")

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital==False:
                shipping=True
        return shipping

    def __str__(self):
        if self.transaction_id == "incomplete":
            return "cart data -->"+self.customer.name
        else:
            return self.transaction_id

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address