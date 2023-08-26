import json
import re
import requests
import simplejson
import urllib
from django.http import *
from django.shortcuts import render, render_to_response,redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout
from bakers.models import Locality, Sub_Locality
from order.models import *
from accounts.models import *
from django.views.decorators.csrf import csrf_exempt
from accounts.utils import *
from datetime import datetime, timedelta, date
from django.core.mail import send_mail, mail_admins
# Create your views here.

def user_login(request):
	username = password = ''
	response_data = {}
	if request.POST and request.is_ajax:
		phone = request.POST['phone']
		password = request.POST['password']
		try:
			get_user_by_phone = UserAccount.objects.get(phone=phone)
			user_phone = get_user_by_phone.phone
			username = get_user_by_phone.user.get_username()
			get_user = User.objects.get(username=username)
			if get_user.check_password(password):
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						response_data = {'login' : "Success"}
					else:
						url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/SMS/" + user_phone + "/AUTOGEN/OTPSEND"
						payload = ""
						response = requests.request("GET", url, data=payload)
						otp_data = response.json()
						response_data['user'] = "not active"
						response_data['user_phone'] = user_phone
			else:
				response_data = {'user':"password wrong"}
		except UserAccount.DoesNotExist:
			response_data = {'user':"nouser"}
	else:
		username = password = ''
		response_data = {'login': "Failed"}
	return HttpResponse(JsonResponse(response_data))

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('%s'%(reverse("userindex")))

def user_signup(request):
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		user_name = request.POST['name']
		user_phone = request.POST['phone']
		user_email = request.POST['email']
		user_password = request.POST['password']
		user_full_name = user_name.split(' ')
		user_first_name = user_full_name[0]
		try:
			user_last_name = user_full_name[1]
		except:
			user_last_name = " "
		user_username = user_name.replace(" ", "").lower()
		url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/SMS/" + user_phone + "/AUTOGEN/OTPSEND"
		payload = ""
		response = requests.request("GET", url, data=payload)
		otp_data = response.json()
		new_user = User.objects.create(username=user_username, email=user_email, first_name=user_first_name, last_name=user_last_name)
		new_user.save()
		new_user.set_password(user_password)
		new_user.is_active = False
		new_user.save()
		log_user = authenticate(username=user_username, password=user_password)
		if log_user is not None:
			login(request, log_user)
		new_profile = UserAccount.objects.get_or_create(user=new_user, phone=user_phone, reward_id=reward_id_generator())
		for key,value in otp_data.items():
			if key == "Details":
				session_id = value
				get_profile = UserAccount.objects.get(user=new_user)
				get_profile.user_otp_session = session_id
				get_profile.save()
		response_data['register'] = "Success"
		message = "Hi Admin! New user "+ str(new_user.get_full_name()) +" has registered with you."
		if response_data['register'] == "Success":
			mail_admins(subject=str(new_user.id)+" new user registration!", message=message, fail_silently=False)
			admin_sms_url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/ADDON_SERVICES/SEND/TSMS" 
			admin_sms_payload = {
				"TemplateName":"Notify-Admin-User-Registration",
				"From": "CKEADM",
				"To": settings.ADMIN_PHONE_NUMBER,
				"VAR1": new_user.get_full_name(),
				"VAR2": get_profile.phone,
				"VAR3": "www.cakemporos.in/admin"
			}
			admin_sms_response = requests.request("POST", admin_sms_url, data=admin_sms_payload)
		response_data['user_phone'] = user_username
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))


@csrf_exempt
def user_otp_verification(request):
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		user_otp = request.POST['otp']
		user_username = request.POST['username']
		get_user = User.objects.get(username=user_username)
		useraccount = UserAccount.objects.get(user=get_user)
		useraccount.user_otp = user_otp
		useraccount.save()
		url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/SMS/VERIFY/" + useraccount.user_otp_session + "/" + user_otp + ""
		payload = ""
		response = requests.request("GET", url, data=payload)		
		otp_data = response.json()
		for key,value in otp_data.items():
			if value == "Success":
				get_user.is_active = True
				get_user.save()
				new_coupon = Coupon.objects.create(coupon_title=get_user.get_username(), coupon_code=useraccount.reward_id, active=True, min_cart_value=350, start_date=datetime.now(), expiry_date=datetime.now()+timedelta(days=30))
				useraccount.coupon.add(new_coupon)
				new_coupon.save()
				response_data = {'verification':'success'}
			if value == "Error":
				logout(request)
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))

@csrf_exempt
def forgotpass_send_otp(request):
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		phone = request.body
		try:
			get_user_by_phone = UserAccount.objects.get(phone=phone)
			username = get_user_by_phone.user.get_username()
			get_user = User.objects.get(username=username)
			url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/SMS/" + phone + "/AUTOGEN/OTPSEND"
			payload = ""
			response = requests.request("GET", url, data=payload)
			otp_data = response.json()
			for key,value in otp_data.items():
				if value == "Success":
					response_data['verification'] = 'success'
					response_data['user_phone'] = phone
				if key == "Details":
					session_id = value
					get_user_by_phone.user_otp_session = session_id
					get_user_by_phone.save()

		except :
			response = {'verfication':'failed'}
		return HttpResponse(JsonResponse(response_data))

@csrf_exempt
def forgotpass_verify_otp(request):
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		user_otp = request.POST['forgotpass_otp']
		user_phone = request.POST['forgotpass_phone']
		get_user_by_phone = UserAccount.objects.get(phone=user_phone)
		session_id = get_user_by_phone.user_otp_session
		url = "http://2factor.in/API/V1/eba5c512-7a7a-11e6-a584-00163ef91450/SMS/VERIFY/" + session_id + "/" + user_otp + ""
		payload = ""
		response = requests.request("GET", url, data=payload)
		
		otp_data = response.json()
		
		for key,value in otp_data.items():
			if value == "Success":
				# authenticate_user = authenticate()
				response_data['verification'] = 'success'
				response_data['username'] = get_user_by_phone.user.get_username()
			if value == "Error":
				response_data = {'verification':'failed'}
				
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))

def user_reset_password(request):
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		user_username = request.POST['username']
		user_password = request.POST['password']
		get_user = User.objects.get(username=user_username)
		get_user.set_password(user_password)
		get_user.save()
		log_user = authenticate(username=user_username, password=user_password)
		if log_user is not None:
			login(request, log_user)
		response_data ={'password_reset':'success'}
		return HttpResponse(JsonResponse(response_data))
	else:
		response_data ={'password_reset':'failed'}
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))

def user_order_history(request):
	user = request.user
	order = Order.objects.filter(user=user)
	get_order_history = OrderHistory.objects.filter(user=user, approve=True).order_by('-timestamp')
	get_shipping_details = OrderShippingDetails.objects.filter(id__in=get_order_history)
	user_full_name = user.get_full_name()
	useraccount = UserAccount.objects.get(user=user)
	user_phone = useraccount.phone
	subtotal = 0
	tax_val = 0
	coupon_code = ""
	coupon_val = 0
	context = {
	"order":order,
	"get_order_history" : get_order_history,
	"get_shipping_details": get_shipping_details,
	"user_full_name" : user_full_name,
	"user_phone" : user_phone,
	"site_name" : "Order History",
	}
	template = "account/order_history.html"
	return render(request, template, context)

def user_new_address(request):
	user = request.user
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		shipping = request.POST['shipping']
		locality = request.POST['locality']
		new_address = UserAddresses.objects.create(user=request.user)
		new_address.user_addresses = shipping
		new_address.user_locality = locality
		new_address.save()
		response_data['get_address'] = shipping
		response_data['get_address_id'] = new_address.id
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))

# def user_password_change(request):
