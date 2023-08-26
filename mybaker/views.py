import operator
import re
import json
import logging
import datetime
import requests
import simplejson
from datetime import datetime, date
from operator import itemgetter, attrgetter
from django.http import JsonResponse

from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.timezone import datetime, timedelta
from django.db.models import Count, Sum
from bakers.models import *
from catalog.models import *
from order.models import *
from cart.models import *
from .forms import LoginForm
today = date.today()
# Create your views here.
def mybaker_logout_view(request):
	logout(request)
	return HttpResponseRedirect('%s'%(reverse("mybaker_login")))

def mybaker_login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/mybaker/dashboard")
	
	form = LoginForm(request.POST or None)
	btn = "Login"
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		messages.success(request, "Successfully Logged In. Welcome Back!")
		return HttpResponseRedirect("/mybaker/dashboard")
	context = {
		"form": form,
		"submit_btn": btn,
	}
	return render(request, "mybaker/login.html", context)

@user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
def mybaker_dashboard(request):
	last_one_days = today - timedelta(days=0)
	last_seven_days = today - timedelta(days=8)
	last_thirty_days = today - timedelta(days=30)
	user = request.user
	baker = get_object_or_404(Baker, owner=user)
	baker_product = Product.objects.filter(baker=baker).order_by('-timestamp')
	cart_items = CartItem.objects.filter(product__in=baker_product).order_by('-timestamp')
	last_seven_days_orders_status = Order.objects.filter(baker=baker, approve=True, order_date__gte=datetime.now()-timedelta(days=7)).order_by('-timestamp')
	happy_customers = Order.objects.filter(baker=baker, approve=True, status="Complete").count()
	baker_product_order_count = Order.objects.filter(baker=baker).values("cartitem__product", "cartitem__product__title", "cartitem__product__image", "cartitem__product__rating_count").annotate(Count("cartitem__product")).order_by("-cartitem__product__count")
	baker_user_order_count = Order.objects.filter(baker=baker).values("user__first_name", "user__last_name").annotate(Count("user")).order_by("-user__count")
	pending_count = 0
	shipped_count = 0
	complete_count = 0
	cancelled_count = 0
	confirmed_count = 0
	ready_count = 0
	baking_count = 0

	for item in last_seven_days_orders_status:
		if item.status == "Pending":
			pending_count += 1
		if item.status == "Cancelled":
			cancelled_count += 1
		if item.status == "Complete":
			complete_count += 1
		if item.status == "Confirmed":
			confirmed_count += 1
		if item.status == "Shipped":
			shipped_count += 1
		if item.status == "Ready":
			ready_count += 1
		if item.status == "Baking":
			baking_count += 1

	sales_last_seven_days = Order.objects.filter(baker=baker, approve=True, order_date__gte=datetime.now()-timedelta(days=7)).values('order_date').annotate(total=Sum('final_total')).order_by('-order_date')
	#total_sales_last_seven_days not being used
	total_sales_last_seven_days = list(sales_last_seven_days)
	sales_total = 0
	for item in sales_last_seven_days:
		sales_total += item['total']


	last_7_days_orders_count = Order.objects.filter(baker=baker, approve=True, order_date__gte=datetime.now()-timedelta(days=7)).values('order_date').annotate(count=Count('id')).order_by('order_date')
	last_7_days_orders_items = list(last_7_days_orders_count)
	dates = [x.get('order_date') for x in last_7_days_orders_count]
	for d in (today - timedelta(days=x) for x in range(0,7)):
		if d not in dates:
	 		last_7_days_orders_items.append({'order_date': d, 'count': 0})
	sorted_order_count = sorted(last_7_days_orders_items, key=itemgetter('order_date'), reverse=False)
	bakers_product_egg_variations = EggVariations.objects.filter(product=baker_product)
	bakers_product_weight_variations = WeightVariations.objects.filter(product=baker_product)
	context = {
		"baker": baker,
		"cart_items": cart_items,
		"baker_product_order_count": baker_product_order_count,
		"baker_user_order_count": baker_user_order_count,
		"sales_total": sales_total,
		"happy_customers": happy_customers,
		"last_seven_days_orders_status": last_seven_days_orders_status,
		"last_7_days_orders_count": last_7_days_orders_count,
		"sorted_order_count": sorted_order_count,
		"bakers_product_egg_variations": bakers_product_egg_variations,
		"bakers_product_weight_variations": bakers_product_weight_variations,
		"final_pending_count":pending_count,
		"final_complete_count":complete_count,
		"final_shipped_count":shipped_count,
		"final_confirmed_count":confirmed_count,
		"final_cancelled_count":cancelled_count,
		"final_ready_count": ready_count,
		"final_baking_count": baking_count
	}
	template = "mybaker/index.html"
	return render(request, template, context)

@user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
def mybaker_orders_list(request):
	user =request.user
	baker = get_object_or_404(Baker, owner=user)
	baker_orders = Order.objects.filter(baker=baker).order_by('-timestamp')
	main_orders = OrderHistory.objects.filter(order=baker_orders, approve=True)
	# auth_url = "http://galvanie.com:3000/api/user/oauth/token"
	# payload = {
	# "username": "cakestar",
	# "password": "password",
	# "client_id": "efOeHY5Ovf",
	# "client_secret": "r18sAsEsxR",
	# "grant_type": "password"
	# }
	# response = requests.request("POST", auth_url, data=payload)
	# if response.status_code == "200" or "201":
	# 	for key, value in response.json().iteritems():
	# 		if key == "access_token":
	# 			baker.access_token = value
	# 			baker.save()
	# 		elif key == "refresh_token" :
	# 			baker.refresh_token = value
	# 			baker.save()
	# else:
	# 	pass

	# url = "http://galvanie.com:3000/api/user/baker/order"
	# payload = {
	# "x-access-token": baker.access_token
	# }
	# response = requests.request("GET", url, headers=payload)
	# logistics_data = response.json()
	# delivery_booking_history = simplejson.loads(response.text)
	context = {
	"baker_name" : baker,
	"baker_orders": baker_orders,
	"page_title": "Orders List",
	"main_orders": main_orders,
	#"delivery_booking_history": delivery_booking_history
	}
	template = "mybaker/order/mybaker_order_list.html"
	return render(request, template, context)

@user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
def mybaker_order_detail(request, order_id):
	user = request.user
	baker = get_object_or_404(Baker, owner=user)
	baker_orders = Order.objects.filter(baker=baker, approve=True).order_by('-timestamp')
	get_order = Order.objects.get(baker=baker, order_id=order_id)
	get_main_order = OrderHistory.objects.filter(order=get_order)
	get_shipping = OrderShippingDetails.objects.get(main_order=get_main_order)
	context = {
	"get_order": get_order,
	"get_main_order": get_main_order,
	"get_shipping": get_shipping,
	"baker": baker,
	"baker_orders": baker_orders,
	"page_title": "Order Detail"
	}
	template = "mybaker/order/mybaker_order_details.html"
	return render(request, template, context)

@csrf_exempt
def mybaker_order_status_update(request, order_id):
 	user = request.user
 	baker = get_object_or_404(Baker, owner=user)
 	get_order = Order.objects.get(baker=baker, order_id=order_id)
 	order_update = {}
 	if request.method == "POST" and request.is_ajax:
 		if 'order_status' not in request.POST:
		    order_status = "Pending"
		else:
		    order_status = request.POST['order_status']

		get_order.status = order_status
		get_order.save()
		order_update['Status'] = "Success"
	return HttpResponse(JsonResponse(order_update))

@user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
def mybaker_payment_clearance(request):
	user = request.user
	baker = get_object_or_404(Baker, owner=user)
	uncleared_payament_orders = Order.objects.filter(payment_clearance=False)
	cleared_payment_orders = Order.objects.filter(payment_clearance=True)
	template = "mybaker/order/mybaker_payment_clear.html"
	context ={
		"baker": baker,
		"uncleared_payament_orders": uncleared_payament_orders,
		"cleared_payment_orders":cleared_payment_orders,
	}
	return render(request, template, context)

@user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
def mybaker_products_list(request):
	user = request.user
	baker = get_object_or_404(Baker, owner=user)
	products = Product.objects.filter(baker=baker)
	template = "mybaker/product/mybaker_product_list.html"
	context ={
	"baker_name" : baker,
	"products":products,
	"page_title": "Products List"
	}
	return render(request, template, context)


# @user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
# def mybaker_add_new_product(request):
# 	username = request.user
# 	baker = Baker.objects.get(owner=username)
# 	category = Category.objects.all()
# 	product_type = ProductType.objects.all()
# 	if request.method == "POST":
# 		if "product_title" not in request.POST:
# 			product_title = None
# 		else:
# 			product_title = request.POST["product_title"]

# 		if "product_by_type" not in request.POST:
# 			product_by_type = 0
# 		else:
# 			product_by_type = request.POST["product_by_type"]

# 		if "product_by_category" not in request.POST:
# 			product_by_category = 0
# 		else:
# 			product_by_category = request.POST["product_by_category"]

# 		if "product_description" not in request.POST:
# 			product_description = None
# 		else:
# 			product_description = request.POST["product_description"]

# 		if "product_starting_price" not in request.POST:
# 			product_starting_price = 0
# 		else:
# 			product_starting_price = request.POST["product_starting_price"]

# 		if "product_veg_or_nonveg" not in request.POST:
# 			product_veg_or_nonveg = None
# 		else:
# 			product_veg_or_nonveg = request.POST["product_veg_or_nonveg"]

# 		if "egg_or_eggless_variant" not in request.POST:
# 			egg_or_eggless_variant = None
# 		else:
# 			egg_or_eggless_variant = request.POST.getlist("egg_or_eggless_variant")

# 		if "egg_or_eggless_price" not in request.POST:
# 			egg_or_eggless_price = 0
# 		else:
# 			egg_or_eggless_price = request.POST["egg_or_eggless_price"]

# 		if "eggless_price" not in request.POST:
# 			eggless_price = 0
# 		else:
# 			eggless_price = request.POST["eggless_price"]

# 		if "weight_variant" not in request.POST:
# 			weight_variant = None
# 		else:
# 			weight_variant = request.POST.getlist("weight_variant")

# 		if "weight_05_price" not in request.POST:
# 			weight_05_price = 0
# 		else:
# 			weight_05_price = request.POST["weight_05_price"]

# 		if "weight_1_price" not in request.POST:
# 			weight_1_price = 0
# 		else:
# 			weight_1_price = request.POST["weight_1_price"]

# 		if "weight_15_price" not in request.POST:
# 			weight_15_price = 0
# 		else:
# 			weight_15_price = request.POST["weight_15_price"]

# 		if "weight_2_price" not in request.POST:
# 			weight_2_price = 0
# 		else:
# 			weight_2_price = request.POST["weight_2_price"]

# 		if "box_variant" not in request.POST:
# 			box_variant = None
# 		else:
# 			box_variant = request.POST.getlist("box_variant")

# 		if "box_1_price" not in request.POST:
# 			box_1_price = 0
# 		else:
# 			box_1_price = request.POST["box_1_price"]

# 		if "box_2_price" not in request.POST:
# 			box_2_price = 0
# 		else:
# 			box_2_price = request.POST["box_2_price"]

# 		if "box_3_price" not in request.POST:
# 			box_3_price = 0
# 		else:
# 			box_3_price = request.POST["box_3_price"]

# 		if "box_4_price" not in request.POST:
# 			box_4_price = 0
# 		else:
# 			box_4_price = request.POST["box_4_price"]

# 		if "box_5_price" not in request.POST:
# 			box_5_price = 0
# 		else:
# 			box_5_price = request.POST["box_5_price"]

# 		if "box_6_price" not in request.POST:
# 			box_6_price = 0
# 		else:
# 			box_6_price = request.POST["box_6_price"]

# 		new_product = Product.objects.create(title=product_title, slug=product_title)
# 		new_product.baker = Baker.objects.get(owner=username)
# 		new_product.product_type = ProductType.objects.get(title=product_by_type)
# 		new_product.category = Category.objects.get(title=product_by_category)
# 		new_product.description = product_description
# 		new_product.starting_price = product_starting_price
# 		new_product.veg_or_nonveg = product_veg_or_nonveg
# 		new_product.save()

# 		# EGG VARIATION 
# 		for item in egg_or_eggless_variant:
# 			if item == "Egg":
# 				new_egg_variant = EggVariations.objects.create(egg_variation_type=item)
# 				new_egg_variant.product = Product.objects.get(id=new_product.id)
# 				new_egg_variant.extra_price = egg_or_eggless_price
# 				new_egg_variant.save()
# 			if item == "Eggless":
# 				new_egg_variant = EggVariations.objects.create(egg_variation_type=item)
# 				new_egg_variant.product = Product.objects.get(id=new_product.id)
# 				new_egg_variant.extra_price = eggless_price
# 				new_egg_variant.save()

# 		# WEIGHT VARIANT SECTION
# 		if weight_variant == None:
# 			pass
# 		else:
# 			for item in weight_variant:
# 				if item == "0_5Kg":
# 					new_weight_variant = WeightVariations.objects.create(weight_variation_type="0.5 Kg")
# 					new_weight_variant.product = Product.objects.get(id=new_product.id)
# 					new_weight_variant.price = weight_05_price
# 					new_weight_variant.save()
# 				if item == "1Kg":
# 					new_weight_variant = WeightVariations.objects.create(weight_variation_type="1 Kg")
# 					new_weight_variant.product = Product.objects.get(id=new_product.id)
# 					new_weight_variant.price = weight_1_price
# 					new_weight_variant.save()
# 				if item == "1_5Kg":
# 					new_weight_variant = WeightVariations.objects.create(weight_variation_type="1.5 Kg")
# 					new_weight_variant.product = Product.objects.get(id=new_product.id)
# 					new_weight_variant.price = weight_15_price
# 					new_weight_variant.save()
# 				if item == "2Kg":
# 					new_weight_variant = WeightVariations.objects.create(weight_variation_type="2 Kg")
# 					new_weight_variant.product = Product.objects.get(id=new_product.id)
# 					new_weight_variant.price = weight_2_price
# 					new_weight_variant.save()

# 		#weight Variation Section
# 		if box_variant == None:
# 			pass
# 		else:
# 			for item in box_variant:
# 				if item == "1_Box":
# 					new_box_variant = BoxVariations.objects.create(box_variation_type="1 Box")
# 					new_box_variant.product = Product.objects.get(id=new_product.id)
# 					new_box_variant.price = box_1_price
# 					new_box_variant.save()
# 					print "Step1"

# 				if item == "2_Box":
# 					new_box_variant = BoxVariations.objects.create(box_variation_type="2 Box")
# 					new_box_variant.product = Product.objects.get(id=new_product.id)
# 					new_box_variant.price = box_2_price
# 					new_box_variant.save()
# 					print "Step2"

# 				if item == "3_Box":
# 					new_box_variant = BoxVariations.objects.create(box_variation_type="3 Box")
# 					new_box_variant.product = Product.objects.get(id=new_product.id)
# 					new_box_variant.price = box_3_price
# 					new_box_variant.save()
# 					print "Step3"

# 				if item == "4_Box":
# 					new_box_variant = BoxVariations.objects.create(box_variation_type="4 Box")
# 					new_box_variant.product = Product.objects.get(id=new_product.id)
# 					new_box_variant.price = box_4_price
# 					new_box_variant.save()
# 					print "Step4"

# 				if item == "5_Box":
# 					new_box_variant = BoxVariations.objects.create(box_variation_type="5 Box")
# 					new_box_variant.product = Product.objects.get(id=new_product.id)
# 					new_box_variant.price = box_5_price
# 					new_box_variant.save()
# 					print "Step5"

# 				if item == "6_Box":
# 					new_box_variant = BoxVariations.objects.create(box_variation_type="6 Box")
# 					new_box_variant.product = Product.objects.get(id=new_product.id)
# 					new_box_variant.price = box_6_price
# 					new_box_variant.save()
# 					print "Step6"

# 		return HttpResponseRedirect('/mybaker/products/')
# 	template = "mybaker/product/mybaker_product_add.html"
# 	context ={
# 		"baker": baker,
# 		"categories": category,
# 		"product_type": product_type
# 	}
# 	return render(request, template, context)

@user_passes_test(lambda u:u.is_staff, login_url='/mybaker/')
def mybaker_update_product(request, slug):
	user = request.user
	baker = get_object_or_404(Baker, owner=user)
	get_product = get_object_or_404(Product, baker=baker, slug=slug)
	get_product_category = get_product.category
	get_product_product_type = get_product.product_type
	egg_variations = EggVariations.objects.filter(product=get_product)
	weight_variations = WeightVariations.objects.filter(product=get_product)
	category = Category.objects.all()
	product_type = ProductType.objects.all()
	if request.method == "POST":
		return HttpResponseRedirect('/mybaker/products/')
	template = "mybaker/product/mybaker_product_update.html"
	context= {
		"baker": baker,
		"get_product": get_product,
		"get_product_category": get_product_category,
		"get_product_product_type":get_product_product_type,
		"egg_variations": egg_variations,
		"categories": category,
		"product_type": product_type,
	}
	return render(request, template, context)