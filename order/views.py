# -*- coding: utf-8 -*-
import time
import requests
import urllib
import math
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, render_to_response, get_object_or_404, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from bakers.models import *
from cart.models import *
from catalog.models import *
from order.models import *
from .utils import *
from accounts.models import *
from django.http import JsonResponse
# Create your views here.

def checkout(request):
	user = request.user
	if user.is_active == False:
		logout(request)
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse("cart"))
	useraccount = UserAccount.objects.get(user=request.user)
	final_amount = 0
	addresses = UserAddresses.objects.filter(user=request.user).order_by('-timestamp')[:3]
	cart_item_count = cart.cartitem_set.all().count()
	cart_item = CartItem.objects.filter(cart=cart)
	cart_subtotal = 0
	for item in cart_item:
		cart_subtotal += item.cart_item_total
		cart.sub_total = cart_subtotal
		cart.save()
	cart.service_charge_value = (cart_subtotal * 0)/100
	cart.total = cart.sub_total + Decimal(cart.service_charge_value) + Decimal(cart.delivery_total)
	cart.save()
	addons = Addon.objects.filter(status=True)
	giftitems = GiftItem.objects.filter(status=True, featured=True)
	if request.method == "POST":
		"""CODE FOR GENERATING INDIVIDUAL BAKER ORDERS WITH ALWAYS NEW ORDER_ID FOR EACH BAKER"""
		if 'prev_shipping_address' not in request.POST:
			prev_add_radio = 0
		else:
			prev_add_radio = request.POST['prev_shipping_address']

		if 'shipping' not in request.POST:
			shipping_a = 0
		else:
			shipping_a = request.POST['shipping']

		if 'delivery_date' not in request.POST:
			delivery_date = 0
		else:
			delivery_date = request.POST['delivery_date']

		if 'delivery_time' not in request.POST:
			delivery_time = 0
		else:
			delivery_time = request.POST['delivery_time']
		payment_method_a = request.POST['payment_method']
		for item in cart_item:
			if (len(cart_item)) == 1:
				try:
					if Order.objects.get(cart=cart, cartitem=item):
						new_order = Order.objects.get(cart=cart, cartitem=item)
						new_order.cart = cart
						new_order.cartitem = item
						new_order.user = request.user
						if item.addon is None:
							new_order.baker = item.product.baker
						else:
							new_order.baker = None
						new_order.sub_total = item.cart_item_total
						new_order.status = "Pending"
						if cart.coupon:
							new_order.discount_total = cart.coupon.coupon_cost
						else:
							new_order.discount_total = 0
						new_order.save()
						final_amount = new_order.get_final_amount()
						new_order.save()
					else:
						new_order = Order()
						new_order.cart = cart
						new_order.cartitem = item
						new_order.user = request.user
						if item.addon is None:
							new_order.baker = item.product.baker
						else:
							new_order.baker = None
						new_order.sub_total = item.cart_item_total
						new_order.order_id = id_generator()
						new_order.status = "Pending"
						if cart.coupon:
							new_order.discount_total = cart.coupon.coupon_cost
						else:
							new_order.discount_total = 0
						new_order.save()
						final_amount = new_order.get_final_amount()
						new_order.save()
					
				except Order.DoesNotExist:
					new_order = Order()
					new_order.cart = cart
					new_order.cartitem = item
					new_order.user = request.user
					if item.addon is None:
						new_order.baker = item.product.baker
					else:
						new_order.baker = None
					new_order.sub_total = item.cart_item_total
					new_order.order_id = id_generator()
					new_order.status = "Pending"
					if cart.coupon:
						new_order.discount_total = cart.coupon.coupon_cost
					else:
						new_order.discount_total = 0
					new_order.save()
					final_amount = new_order.get_final_amount()
					new_order.save()
					
			else:
				try:
					if Order.objects.get(cart=cart, cartitem=item):
						new_order = Order.objects.get(cart=cart, cartitem=item)
						new_order.cart = cart
						new_order.cartitem = item
						new_order.user = request.user
						if item.addon is None:
							new_order.baker = item.product.baker
						else:
							new_order.baker = None
						new_order.sub_total = item.cart_item_total
						new_order.status = "Pending"
						if cart.coupon:
							new_order.discount_total = cart.coupon.coupon_cost
						else:
							new_order.discount_total = 0
						new_order.save()
						final_amount = new_order.get_final_amount()
						new_order.save()
					else:
						new_order = Order()
						new_order.cart = cart
						new_order.cartitem = item
						new_order.user = request.user
						if item.addon is None:
							new_order.baker = item.product.baker
						else:
							new_order.baker = None
						new_order.sub_total = item.cart_item_total
						new_order.order_id = id_generator()
						new_order.status = "Pending"
						if cart.coupon:
							new_order.discount_total = cart.coupon.coupon_cost
						else:
							new_order.discount_total = 0
						new_order.save()
						final_amount = new_order.get_final_amount()
						new_order.save()
					
				except Order.DoesNotExist:
					new_order = Order()
					new_order.cart = cart
					new_order.cartitem = item
					new_order.user = request.user
					if item.addon is None:
						new_order.baker = item.product.baker
					else:
						new_order.baker = None
					new_order.sub_total = item.cart_item_total
					new_order.order_id = id_generator()
					new_order.status = "Pending"
					if cart.coupon:
						new_order.discount_total = cart.coupon.coupon_cost
					else:
						new_order.discount_total = 0
					new_order.save()
					final_amount = new_order.get_final_amount()
					new_order.save()
					
		new_history = OrderHistory()
		new_history.main_order_id = main_id_generator()
		new_history.user = request.user
		new_history.save()

		order_ship_detail = OrderShippingDetails.objects.create(user=request.user)
		order_ship_detail.user = new_order.user
		order_ship_detail.main_order = new_history
		order_ship_detail.save()
		if shipping_a:
			order_ship_detail.shipping_address = shipping_a
		elif prev_add_radio:
			order_ship_detail.shipping_address = prev_add_radio
 		order_ship_detail.payment_method = payment_method_a
 		order_ship_detail.delivery_date = delivery_date
 		order_ship_detail.delivery_time = delivery_time
		order_ship_detail.save()

		
		for orders in Order.objects.filter(cart=cart):
			new_history.order.add(orders)
			new_history.save()

		if cart.coupon is not None:
			useraccount.coupon.add(cart.coupon)
			useraccount.save()
		else:
			pass
			
		return HttpResponseRedirect(reverse("order_confirm"))
		
	context = {
	"cart": cart,
	"addresses":addresses,
	"cart_subtotal":cart_subtotal,
	"site_name": "Checkout",
	"useraccount": useraccount,
	"addons":addons,
	"giftitems": giftitems,
	"S3_URL" : settings.S3_URL
	}
	template = "orders/checkout.html"
	return render(request, template, context)

def order_confirm(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse("cart"))
	user = request.user
	get_useraccount = UserAccount.objects.get(user=user)
	get_user_phone = get_useraccount.phone
	get_user_email = user.email
	get_user_first_name = user.get_short_name()
	user_fullname = user.get_full_name()
	recent_order = OrderHistory.objects.filter(user=user).order_by('-timestamp')[:1]
	for item in recent_order:
		order_list = item.order
		VAR2 = item
		VAR3 = item.get_all_final_total()
		user_order_id = item
		order_ship_details = OrderShippingDetails.objects.get(main_order=item)
		for orders in order_list.all():
			if orders.baker is None:
				pass
			else:
				get_baker_user = User.objects.get(username=orders.baker.owner)
				get_baker_account = UserAccount.objects.get(user=get_baker_user)
				get_baker_phone = get_baker_account.phone
				get_baker_email = get_baker_user.email
	"""Bit.ly URL"""
	bitly_url = "https://api-ssl.bitly.com/v3/shorten"
	bitly_param = {
		"access_token" : "f0917bc54386679c3ada6ba6ca2fe72edeb3d9ca",
		"longUrl" : "http://" + settings.DOMAIN_NAME + "/superadmin/order_detail/" + str(user_order_id)
	}
	bitly_response = requests.request("GET", bitly_url, headers=None, params=bitly_param)
	bitly_response_content = simplejson.loads(bitly_response.text)
	"""SMS URL"""
	VAR4 =  bitly_response_content['data']['url'],
	

	url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/ADDON_SERVICES/SEND/TSMS"
	payload = {
		"TemplateName":"SuperAdmin-Order-Notification",
		"From": "CKEADM",
		"To": settings.ADMIN_PHONE_NUMBER,
		"VAR1": get_user_first_name,
		"VAR2": VAR2,
		"VAR3": VAR3,
		"VAR4": VAR4
	}
	response = requests.request("POST", url, data=payload)
	trans_data = response.json()
	html_email = get_template("orders/order_email.html")
	subject = "Your order #" + str(user_order_id) + " confirmed with Cakemporos!"
	to_list = [get_user_email, "nikhil.salome@gmail.com", "cakemporos.in@gmail.com"]
	from_email = settings.EMAIL_HOST_USER
	message = "Order #" + str(user_order_id) + " placed successfully with Cakemporos"
	
	site_name = "Order Confirmation"
	context = {
		"recent_order":recent_order,
		"order_list": order_list,
		"user_order_id": user_order_id,
		"site_name": site_name,
		"cart":cart,
		"user_fullname": user_fullname,
		"order_ship_details": order_ship_details
	}
	template = "orders/order_confirm.html"
	# html_content = html_email.render(context)
	# send_email = EmailMultiAlternatives(subject, message, from_email, to_list)
	# send_email.attach_alternative(html_content, "text/html")
	# send_email.send()
	del request.session['cart_id']
	return render(request, template, context)

@csrf_exempt
def calculate_delivery_charge(request, id):
	get_address = get_object_or_404(UserAddresses, id=id)
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
	response_data = {}
	if request.is_ajax:
		origins = str(cart.locality)
		destinations = str(get_address.user_locality)
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins="+origins+"&destinations="+destinations+"&key=AIzaSyCRcKLBQYizfeHi8fc1GzihE5TK4KTOYEY"
		googleResponse = urllib.urlopen(url)
		jsonResponse = simplejson.loads(googleResponse.read())
		get_distance = jsonResponse['rows'][0]['elements'][0]['distance']['text']
		first = get_distance.split()
		cart_item_count = cart.cartitem_set.all().count()
		delivery_total = 0
		cart_weight = 0.0
		for item in cart.cartitem_set.all():
			weight = item.weight.weight_variation_type.split(" ")
			weight_value = float(weight[0])
			cart_weight += float(weight_value) * item.quantity
		cart.total_cart_weight = cart_weight
		cart.save()
		print cart.total_cart_weight
		if cart.total_cart_weight <= 1:
			if float(first[0]) <= 10.0:
				delivery_type = "Hyperlocal"
				if float(first[0]) <= 3:
					delivery_total = 60
				else:
					delivery_total = 60+((float(first[0])-3.0)*12)
			else:
				delivery_type = "Long Distance"
				delivery_total = 200
		else:
			if float(first[0]) <= 5:
					delivery_total = 250
			else:
				delivery_total = 200+((float(first[0])-5.0)*15)

		cart.delivery_total = delivery_total
		cart.save()
		cart_item = CartItem.objects.filter(cart=cart)
		cart_subtotal = 0
		for item in cart_item:
			cart_subtotal += item.cart_item_total
			cart.sub_total = cart_subtotal
			cart.save()
		if cart.coupon:
			code = get_object_or_404(Coupon, coupon_code=cart.coupon.coupon_code)
			cart.sub_total = cart.sub_total - code.coupon_cost
			response_data['coupon'] = "("+str(cart.coupon)+")" +" "+ "(₹ "+str(cart.coupon.coupon_cost)+" )"
			cart.save()
		else:
			response_data['coupon'] = "-"
		cart.service_charge_value = (cart_subtotal * 0)/100
		cart.total = cart.sub_total + Decimal(cart.service_charge_value) + Decimal(cart.delivery_total)
		cart.save()
		response_data['delivery_total'] = "₹ "+str(cart.delivery_total)
		response_data['distance'] = get_distance
		response_data['cart_sub_total'] = "₹ "+str(cart.sub_total)
		response_data['cart_total'] = "₹ "+str(math.ceil(cart.total))
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))