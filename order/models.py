import requests
import simplejson
from decimal import Decimal
from django.conf import settings
from django.db import models
# Create your models here.
from cart.models import *
# from accounts.models import *
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Avg
from accounts.models import UserAccount

DELIVERY_METHOD = (
	("Home Delivery", "Home Delivery"),
	("Store Pickup","Store Pickup"),
	)

PAYMENT_METHOD = (
	("Cash On Delivery", "Cash On Delivery"),
	("Pay Online", "Pay Online"),
	)

STATUS_CHOICES = (
		("Pending", "Pending"),
		("Confirmed", "Confirmed"),
		("Baking", "Baking"),
		("Shipped","Shipped"),
		("Complete", "Complete"),
		("Cancelled", "Cancelled"),
		("Ready", "Ready"),
	)
try:
	tax_rate = settings.DEFAULT_TAX_RATE
except Exception, e:
	print str(e)
	raise NotImplementedError(str(e))
	
class OrderManager(models.Manager):
	def get_order_id(self):
		return self.order_id

	def get_product(self):
		return self.cartitem.product

	def get_product_weight(self):
		return self.cartitem.weight

class Order(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	baker = models.ForeignKey(Baker, blank=True, null=True)
	order_id = models.CharField(max_length=120, default='ABCDE', unique=True)
	cart = models.ForeignKey(Cart)
	cartitem = models.ForeignKey(CartItem, blank=True, null=True)
	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Pending")
	sub_total = models.DecimalField(default=10.99, max_digits=50, decimal_places=2)
	discount_total = models.DecimalField(default=00.00, max_digits=50, decimal_places=2)
	tax_total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	final_total = models.DecimalField(default=10.99, max_digits=50, decimal_places=2)
	order_date = models.DateField(auto_now_add=True, auto_now=False)
	approve = models.BooleanField(default=False)
	notify_baker = models.BooleanField(default=False)
	notes = models.TextField(blank=True, null=True)
	tracking_id = models.CharField(max_length=100, blank=True, null=True)
	payment_clearance = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	objects = models.Manager()
	order_manager = OrderManager()
 
	class Meta:
		ordering = ["-timestamp"]
		unique_together = ("id", "order_id")

	def __unicode__(self):
		return self.order_id

	def save(self, *args, **kwargs):
		if self.approve == True and self.notify_baker == True:
			get_baker_account = UserAccount.objects.get(user=self.baker.owner)
			"""Bit.ly URL"""
			bitly_url = "https://api-ssl.bitly.com/v3/shorten"
			bitly_param = {
				"access_token" : "f0917bc54386679c3ada6ba6ca2fe72edeb3d9ca",
				"longUrl" : "http://" + settings.DOMAIN_NAME + "/mybaker/orders/order_detail/" + self.order_id
			}
			bitly_response = requests.request("GET", bitly_url, headers=None, params=bitly_param)
			bitly_response_content = simplejson.loads(bitly_response.text)
			main_order_id = self.orderhistory_set.all()
			get_shipping_details = OrderShippingDetails.objects.get(main_order=main_order_id)
			if self.cartitem.cupcake_qty:
				cupcake_qty = self.cartitem.cupcake_qty
			else:
				cupcake_qty = "No"
			if self.cartitem.photo_cake_image:
				photocake = "Yes"
			else:
				photocake = "No"
			if self.cartitem.msg_on_cake:
				msg_on_cake = self.cartitem.msg_on_cake
			else:
				msg_on_cake = "No MSG"
			sms_payload = {
				"TemplateName": "Notify-Baker-Upon-Order-Delivery",
				"From": "CAKEMP",
				"To": get_baker_account.phone,
				"VAR1": self.baker.owner,
				"VAR2": self.order_id,
				"VAR3": self.cartitem.product,
				"VAR4": self.cartitem.weight,
				"VAR5": self.cartitem.quantity,
				"VAR6": cupcake_qty,
				"VAR7": self.cartitem.egg_or_eggless,
				"VAR8": msg_on_cake,
				"VAR9": photocake,
				"VAR10": "%s at %s" %(get_shipping_details.delivery_date, get_shipping_details.delivery_time),
				"VAR11": bitly_response_content['data']['url'],
				"VAR12": "9766526943",
			}
			sms_response = requests.request("POST", settings.TRANSACTIONAL_SMS_URL, data=sms_payload)
			self.notify_baker = False
			self.notes = "Baker was notified at"+ str(self.updated)
		super(Order, self).save(*args, **kwargs)

	def get_final_amount(self):
		instance = Order.objects.get(id=self.id)
		two_places = Decimal(10) ** -2
		tax_rate_dec = Decimal("%s" %(tax_rate))
		sub_total_dec = instance.sub_total
		discount_total_dec = instance.discount_total
		tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
		instance.tax_total = tax_total_dec
		instance.final_total = sub_total_dec - discount_total_dec
		instance.save()
		return instance.final_total

class OrderHistory(models.Model):
	main_order_id = models.CharField(max_length=120, default='ABC12', unique=True)
	user = models.ForeignKey(User, blank=True, null=True)
	order = models.ManyToManyField(Order, default="")
	approve = models.BooleanField(default=False)
	notify_customer = models.BooleanField(default=False)
	notes = models.TextField(blank=True, null=True)
	ask_customer_for_feedback = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	
	class Meta:
		get_latest_by = "user"
		unique_together = ("id", "main_order_id")

	def __unicode__(self):
		return self.main_order_id

	# To display orders list in the admin panel.
	def orders_list(self):
		return ",\n".join([s.order_id for s in self.order.all()])

	def get_all_sub_total(self):
		sub_total = 0
		for item in self.order.all():
			sub_total += item.sub_total
		return sub_total 

	def get_all_tax_total(self):
		tax_total = 0
		for item in self.order.all():
			tax_total += item.tax_total
		return tax_total

	def get_all_discount_total(self):
		discount_total = 0
		for item in self.order.all():
			discount_total += item.discount_total
		return discount_total

	def get_all_final_total(self):
		all_final_total = 0
		delivery_total = 0
		for item in self.order.all():
			all_final_total += item.get_final_amount()
			cart = item.cart
			delivery_total = cart.delivery_total
		self.final_total = all_final_total + delivery_total
		return self.final_total

	def save(self, *args, **kwargs):
		get_user_account = UserAccount.objects.get(user=self.user)
		if self.approve == True and self.notify_customer == True:
			payload = {
				"TemplateName":"Order Placed",
				"From": "CKMPRS",
				"To": get_user_account.phone,
				"VAR1": self.user.get_short_name(),
				"VAR2": self.main_order_id,
				"VAR3": self.get_all_final_total()
			}
			response = requests.request("POST", settings.TRANSACTIONAL_SMS_URL, data=payload)
			self.notify_customer = False
			self.notes = "Customer was notified " + str(self.updated)
		if self.ask_customer_for_feedback == True:
			payload = {
				"TemplateName":"cakemporos-customer-feedback",
				"From": "CKMPRS",
				"To": get_user_account.phone,
				"VAR1": self.user.get_short_name(),
				"VAR2": "https://cakemporos.typeform.com/to/VTMvaw"
			}
			response = requests.request("POST", settings.TRANSACTIONAL_SMS_URL, data=payload)
			self.ask_customer_for_feedback = False
		super(OrderHistory, self).save(*args, **kwargs)


class OrderShippingDetails(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	main_order = models.ForeignKey('OrderHistory', blank=True, null=True)
	delivery_date = models.CharField(max_length=120, default="")
	delivery_time = models.CharField(max_length=120, default="")
	shipping_address = models.TextField(default="")
	payment_method = models.CharField(max_length=20, default="Cash On Delivery")
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.shipping_address
		

