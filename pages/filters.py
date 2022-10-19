import django_filters
from django_filters import DateFilter,CharFilter,RangeFilter
from . models import *



class ProductFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name',lookup_expr='icontains')
	price_from = RangeFilter(field_name='price',lookup_expr='gte')
	price_to = RangeFilter(field_name='price',lookup_expr='lte')
	
	class Meta:
		model = Product
		fields='__all__'
		exclude=['product_pic','date_created','name','price']



class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='date_added',lookup_expr='gte')
	end_date = DateFilter(field_name='date_added',lookup_expr='lte')
	
	class Meta:
		model = CartItem
		fields='__all__'
		exclude=['quantity','date_added']