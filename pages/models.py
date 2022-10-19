from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User,null =True,on_delete = models.CASCADE)
	name = models.CharField(max_length = 200,null = True)
	phone = models.CharField(max_length = 200,null=True)
	email = models.CharField(max_length = 200,null=True)
	profile_pic = models.ImageField(default = 'profile.png',null=True,blank = True)
	date_created = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length = 200,null = True)

	def __str__(self):
		return self.name



class Product(models.Model):
	CATEGORY= (
		('Wine','Wine'),
		('Dine','Dine'),
		)	
	name = models.CharField(max_length = 200,null = True)
	price = models.FloatField(null=True)
	product_pic = models.ImageField(default = 'no.png',null=True,blank = True)
	category = models.CharField(max_length = 200,null=True,choices = CATEGORY)
	description = models.CharField(max_length = 500,null=True,blank = True)
	date_created = models.DateTimeField(auto_now_add = True)
	tags = models.ManyToManyField(Tag)	
	def __str__(self):
		return self.name

class Order(models.Model):
	
	customer = models.ForeignKey(Customer, null = True , on_delete = models.SET_NULL)
	product = models.ForeignKey(Product, null = True , on_delete = models.SET_NULL)
	
	date_ordered = models.DateTimeField(auto_now_add = True)
	
	transaction_id = models.CharField(max_length = 200,null=True)

	def __str__(self):
		return str(self.customer.name)+"'s Order"


	@property
	def total_cart(self):
		orderitems = self.cartitem_set.all()
		total= sum([item.get_total for item in orderitems ])
		return total

	@property
	def total_cart_items(self):
		orderitems = self.cartitem_set.all()
		total= sum([item.quantity for item in orderitems ])
		return total				


class CartItem(models.Model):
	STATUS = (
		('Pending','Pending'),
		
		('Delivered','Delivered'),
		)
	product = models.ForeignKey(Product, null = True ,blank=True, on_delete = models.SET_NULL)
	order = models.ForeignKey(Order, null = True ,blank=True, on_delete = models.SET_NULL)
	quantity = models.IntegerField(default=0,null=True,blank=True)
	status = models.CharField(max_length = 200,null=True,blank=True,choices=STATUS ,default='Pending')
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return str(self.product.name)

	@property
	def get_total(self):
		total= self.product.price * self.quantity
		return total



class Shipping(models.Model):
	order = models.ForeignKey(Order, null = True ,blank=True, on_delete = models.SET_NULL)
	customer = models.ForeignKey(Customer, null = True ,blank=True, on_delete = models.SET_NULL)
	address1 = models.CharField(max_length = 200,null = True)
	address2 = models.CharField(max_length = 200,null = True,blank=True)
	city = models.CharField(max_length = 200,null = True)
	pincode = models.CharField(max_length = 200,null = True)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.address1	


# class BackGround(models.Model):
	# product_pic = models.ImageField(default = 'no.png',null=True,blank = True)
