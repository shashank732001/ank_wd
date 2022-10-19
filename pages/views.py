from django.shortcuts import render,redirect
from .models import *
from .forms import *
from . filters import *

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.

#login and authentication
@unauthenticated_user
def login(request):

	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username = username,password = password)

		if user is not None:
			auth_login(request, user)
			return redirect('home')
		else:
			messages.info(request,'Username or Password incorrect')


	context = {}
	return render(request,'pages/login.html',context)


@unauthenticated_user
def register(request):

	form = CreateUserForm()
	if request.method =='POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			

			messages.success(request,'Account was successfully created for  '+ str(user))
			return redirect('login')
	context = {'form':form,}
	return render(request,'pages/register.html',context)


def logout(request):

	auth_logout(request)
	return redirect('login')	






#Page Views
@login_required(login_url='login')
def homepage(request):
	orders = Order.objects.all()
	orders1 = CartItem.objects.all()
	customer1 = request.user.customer
	customers = Customer.objects.all()
	
	total_customers = customers.count()
	
	order, created = Order.objects.get_or_create(customer=customer1,)
	cartItems = order.total_cart_items
	items= order.cartitem_set.all()
	item_pending_count = items.filter(status='Pending').count()
	# print(orders1)
	# print('-----------')
	# print(orders)
	context = {
	
	'orders':orders1,
	'customers':customers,
	'total_customers':total_customers,
	'item_pending_count':item_pending_count,
	'cartItems':cartItems,
	}

	return render(request,'pages/homepage.html',context)

@login_required(login_url='login')
def productpage(request):
	products=Product.objects.all()
	customer1 = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer1,)
	cartItems = order.total_cart_items
	items= order.cartitem_set.all()
	item_pending_count = items.filter(status='Pending').count()
	myFilter = ProductFilter(request.GET,queryset=products)
	products=myFilter.qs
	context={
	'item_pending_count':item_pending_count,
	'products':products,
	'cartItems':cartItems,
	'myFilter':myFilter,
	}
	return render(request,'pages/products.html',context)



@login_required(login_url='login')
def statuspage(request):
	
	all_orders = Order.objects.all()
	all_orders1 = CartItem.objects.all()
	# print(all_orders.count())
	orders = request.user.customer.order_set.all()
	customer1 = request.user.customer
	
	total_orders1 = all_orders1.count()
	delivered1 = all_orders1.filter(status='Delivered').count()
	pending1 = all_orders1.filter(status='Pending').count()
	order, created = Order.objects.get_or_create(customer=customer1,)
	cartItems = order.total_cart_items
	items= order.cartitem_set.all()
	myFilter = OrderFilter(request.GET,queryset=all_orders1)
	all_orders1=myFilter.qs
	
	item_pending_count = items.filter(status='Pending').count()
	total_orders = items.count()
	delivered = items.filter(status='Delivered').count()
	pending = items.filter(status='Pending').count()
	myFilter1 = OrderFilter(request.GET,queryset=items)
	items=myFilter1.qs

	
	context = {
	'myFilter':myFilter,
	'myFilter1':myFilter1,
	'item_pending_count':item_pending_count,
	'items':items,
	'all_orders':all_orders1,
	'orders':orders,
	'total_orders':total_orders,
	'delivered':delivered,
	'pending':pending,
	'total_orders1':total_orders1,
	'delivered1':delivered1,
	'pending1':pending1,
	'cartItems':cartItems,
	}	
	return render(request,'pages/status.html',context)	




@login_required(login_url='login')
def dashboardpage(request):
	user1 = request.user.customer
	form = CustomerForm(instance=user1)
	order, created = Order.objects.get_or_create(customer=user1,)
	cartItems = order.total_cart_items
	items= order.cartitem_set.all()
	item_pending_count = items.filter(status='Pending').count()

	if request.method == 'POST':
		form = CustomerForm(request.POST,request.FILES,instance=user1)
		if form.is_valid():
			form.save()

	context = {'form':form,
	'item_pending_count':item_pending_count,
	'cartItems':cartItems,
	}
	return render(request,'pages/dashboard.html',context)



#cart and checkout views
@login_required(login_url='login')
def cart(request):
	
	customer1 = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer1,)
	items= order.cartitem_set.all()
	cartItems = order.total_cart_items
	item_pending = items.filter(status='Pending')
	item_delivered = items.filter(status='Delivered')
	item_pending_count = items.filter(status='Pending').count()
	
	# print(items)
	# print(item_pending)
	# print(item_pending_count)
	context={
	'item_pending_count':item_pending_count,
	'item_delivered':item_delivered,
	'item_pending':item_pending,
	'items':items,
	'order':order,
	'cartItems':cartItems,
	}
	return render(request,'pages/cart.html',context)


@login_required(login_url='login')
def checkout(request):
	customer1 = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer1,)
	items= order.cartitem_set.all()
	cartItems = order.total_cart_items
	item_pending_count = items.filter(status='Pending').count()
	# print(cartItems)
	context={
	'item_pending_count':item_pending_count,
	'items':items,
	'order':order,
	'cartItems':cartItems,
	}
	return render(request,'pages/checkout.html',context)	



def updateItem(request):

	data=json.loads(request.body)
	productId=data['productId']
	action=data['action']

	# print('Action:',action)
	# print('product-id:',productId)

	customer= request.user.customer
	product=Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer,)

	cartItem, created = CartItem.objects.get_or_create(order=order,product=product)


	if action =='add':
		cartItem.quantity = (cartItem.quantity + 1)

	elif action =='remove':
		cartItem.quantity = (cartItem.quantity - 1)

	cartItem.save()	

	if cartItem.status == 'Delivered':
		cartItem.delete()

	if cartItem.quantity <= 0:
		cartItem.delete()


		
	return JsonResponse("item was added", safe=False)


def cartitemUpdate(request,pk):
	item = CartItem.objects.get(id=pk)
	form = ItemForm(instance=item)
	if request.method == 'POST':
		form = ItemForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('/status')
	context={
	'form':form,
	}
	return render(request,'pages/update-status.html',context)


def cartitemDelete(request,pk):
	item = CartItem.objects.get(id=pk)
	
	if request.method == 'POST':
		
		item.delete()
		return redirect('/status')
	context={
	'item':item,
	}
	return render(request,'pages/delete-cart-item.html',context)	


def addProduct(request):

	form = ProductForm()
	if request.method =='POST':
		form = ProductForm(request.POST,request.FILES)
		if form.is_valid():
			product = form.save()
			return redirect('products')
	context = {'form':form,}
	return render(request,'pages/add-product.html',context)



def editProduct(request,pk):
	product = Product.objects.get(id=pk)

	form = ProductForm(instance=product)
	if request.method == 'POST':
		form = ProductForm(request.POST,request.FILES,instance=product)
		if form.is_valid():
			form.save()
			return redirect('/products')
	context = {'form':form,}
	return render(request,'pages/edit-product.html',context)



def viewProduct(request,pk):
	product = Product.objects.get(id=pk)
	context = {'product':product,}
	return render(request,'pages/view-product.html',context)