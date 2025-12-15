from django.db import models


# Create your models here.

    
class Register(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(unique=True,blank=True,null=True)
    password=models.CharField(max_length=10,blank=True,null=True)
    otp=models.CharField(max_length=5,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10,blank=True,null=True)
    discount = models.IntegerField(default=100,blank=True,null=True)
    expiry_time = models.DateTimeField(blank=True,null=True)

    def __str__(self):
         return self.coupon_code

class User_coupon(models.Model):
    user_id=models.ForeignKey(Register,max_length=60,on_delete=models.CASCADE,blank=True,null=True)
    coupon_id=models.ForeignKey(Coupon,max_length=60,on_delete=models.CASCADE,blank=True,null=True)
    ex=models.BooleanField(blank=True,null=True) 
    expiry_time = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.coupon_id.coupon_code

class Main_Category(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    
    
class Sub_Category(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
            return self.name
    
class Color(models.Model):    
    name = models.CharField(max_length=10,blank=True,null=True)
    
    def __str__(self):
            return self.name
    
    
class Product(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE,blank=True,null=True)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,blank=True,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    image = models.ImageField(upload_to="media",blank=True,null=True)
    price = models.FloatField(blank=True,null=True)
    old_price = models.FloatField(blank=True,null=True)
    descriptions = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    
class Contect(models.Model):
    name = models.CharField(max_length=30,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    subject =models.CharField(max_length=70,blank=True,null=True)
    message =models.TextField(blank=True,null=True)

    def __str__(self):
         return self.name
    


         
class Add_cart(models.Model):

    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    img = models.ImageField(upload_to="media",blank=True,null=True)
    price = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField(blank=True,null=True)
    total_price = models.IntegerField(blank=True,null=True)

    def __str__(self):
         return self.name
    
class Wish_list(models.Model):
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,blank=True,null=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    price = models.IntegerField(blank=True,null=True)
    img = models.ImageField(upload_to="media",blank=True,null=True)

class Checkout(models.Model):
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    company_name = models.CharField(max_length=50,blank=True,null=True)
    phone = models.IntegerField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    address1 = models.CharField(max_length=100,blank=True,null=True)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=20,blank=True,null=True)
    district = models.CharField(max_length=20,blank=True,null=True)
    pincode = models.IntegerField(blank=True,null=True)
    note = models.TextField(blank=True,null=True)
    
    def __str__(self):
         return self.first_name

class Order(models.Model):
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    order_id = models.CharField(max_length=20,blank=True,null=True)
    quantity = models.CharField(max_length=50,blank=True,null=True)
    price = models.IntegerField(blank=True,null=True)
    # subtotal = models.IntegerField(blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return self.user_id.name
class tichers (models.Model):
    name = models.CharField(max_length=20,blank=True,null=True)
    selery = models.IntegerField(blank=True,null=True)
class student (models.Model):
    tid = models.ForeignKey(tichers,on_delete=True,blank=True,null=True)
    name = models.CharField(max_length=20,blank=True,null=True)
