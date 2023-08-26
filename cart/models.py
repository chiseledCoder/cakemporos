from django.db import models
from decimal import Decimal
from catalog.models import *
from django.conf import settings
from django.core.urlresolvers import reverse
from sales.models import Coupon
from bakers.models import *
CART_WEIGHT = (
	("0.5 Kg"," 0.5 Kg"),
	("1 Kg","1 Kg"),
	("1.5 Kg"," 1.5 Kg"),
	("2 Kg","2 Kg")
	)

class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product, null=True, blank=True)
	addon = models.ForeignKey(Addon, null=True, blank=True)
	addon_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	addon_qty = models.IntegerField(default=1)
	giftitem = models.ForeignKey(GiftItem, null=True, blank=True)
	giftitem_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	giftitem_qty = models.IntegerField(default=1)
	quantity = models.IntegerField(default=1)
	weight = models.ForeignKey(WeightVariations, null=True, blank=True)
	weight_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	cupcake_qty = models.ForeignKey(BoxVariations, null=True, blank=True)
	cupcake_qty_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	egg_or_eggless = models.ForeignKey(EggVariations, null=True, blank=True)
	egg_or_eggless_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	msg_on_cake = models.TextField(default="", null=True, blank=True)
	photo_cake_image = models.ImageField(upload_to='cartitem/photocakes/', null=True, blank=True)
	photo_cake_cost = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	cart_item_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	delivery_cost = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	line_total = models.DecimalField(default=10.99, max_digits=50, decimal_places=2)
	notes = models.TextField(null=True, blank=True)
	commission_percentage = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	payout_amount = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)


	def __unicode__(self):
		try:
			return "Cart id: %s  (Product: %s -by %s)" %(str(self.cart.id), self.product.title, self.product.baker)
		except:
			return "Cart id: %s  (Addon: %s)" %(str(self.cart.id), self.addon.title)

	def save(self, *args, **kwargs):
		commission_rate = Decimal(self.commission_percentage)
		cart_value = Decimal(self.cart_item_total)
		difference_value = ((cart_value * commission_rate)/100)
		pay_amt = cart_value - difference_value
		self.payout_amount = Decimal(pay_amt)
		super(CartItem, self).save(*args, **kwargs)

	# def get_absolute_url(self):
	# 	return reverse('myadmin_cartitem_detail', kwargs={"id": self.id})

class Cart(models.Model):	
	service_charge_value = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	sub_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	delivery_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	coupon = models.ForeignKey(Coupon, blank=True, null=True)
	locality = models.ForeignKey(Locality, blank=True, null=True)
	total_cart_weight = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "Cart id: %s" %(self.id)

	def get_absolute_url(self):
		return reverse('myadmin_cart_detail', kwargs={"id": self.id})

	def get_products_list(self):
		return ",\n".join([c.self for c in self.cartitem.all()])