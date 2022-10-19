from django.forms import ModelForm
from .models import *
from django.forms import ModelForm, TextInput, EmailInput,FileInput,NumberInput,ModelMultipleChoiceField


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class ItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'   

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__' 
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Product Name'
                }),
            'price': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Price of the product'
                }),
            
            'product_pic': FileInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Choose or drag and drop the product picture'
                }),
            'description': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; min-height:30px;',
                'placeholder': 'Product Description'
                }),
            
            'tags': forms.CheckboxSelectMultiple

            }

        category= forms.ModelChoiceField(Product.objects.all(),empty_label=None)
        labels = {
            'category':'Category',
            'tags': 'CHOOSE TAGS FOR THE PRODUCT'
        }



class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']
		widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            'phone': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Phone Number'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
            'profile_pic': FileInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Choose or drag and drop your profile picture'
                }),
            }


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']