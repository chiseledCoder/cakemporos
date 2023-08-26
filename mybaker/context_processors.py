from catalog.models import *
from bakers.models import Baker
from order.models import Order
from django.db.models import Count, Sum

def baker_products(request):
	try:
		baker = request.user
		get_baker = Baker.objects.get(owner=baker)
		get_products = Product.objects.filter(baker=get_baker).order_by('timestamp')
		get_products_count = get_products.count()
	except:
		get_products = None
		get_products_count = None
	return {
		"get_products": get_products,
		"get_products_count": get_products_count,
	}

def baker_orders(request):
	try:
		baker = request.user
		get_baker = Baker.objects.get(owner=baker)
		get_orders = Order.objects.filter(baker=get_baker, approve=True).order_by('-timestamp')
		get_orders_count = get_orders.count()
	except:
		get_orders = None
		get_orders_count = None
	return {
		"get_orders": get_orders,
		"get_orders_count": get_orders_count
	}

def baker_sales(request):
	try:
		baker = request.user
		get_baker = Baker.objects.get(owner=baker)
		get_orders = Order.objects.filter(baker=get_baker, approve=True)
		get_total_sales = 0
		for item in get_orders:
			get_total_sales += item.get_final_amount()
	except:
		get_total_sales = None
	return {
		"get_total_sales": get_total_sales
		
	}

def baker_customers(request):
	try:
		baker = request.user
		get_baker = Baker.objects.get(owner=baker)
		get_total_users = Order.objects.filter(baker=get_baker, approve=True).annotate(total=Count('user'))
	except:
		get_total_users = None
	return {
		"get_total_users":get_total_users,
	}