from django.db import models
from bakers.models import *
from catalog.models import *
# Create your models here.

DISCOUNT_TYPE = (
		("Fixed Amount", "Fixed Amount"),
		("Percentage", "Percentage"),
	)
class Coupon(models.Model):
	coupon_title = models.CharField(max_length=200)
	coupon_code = models.CharField(max_length=20)
	start_date = models.DateTimeField(blank=True, null=True)
	expiry_date = models.DateTimeField(blank=True, null=True)
	active = models.BooleanField(default=False)
	description = models.TextField(blank=True, null=True)
	min_cart_value = models.IntegerField(default="0")
	discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE, default="")
	coupon_cost = models.IntegerField(default="0")
	usage_per_person = models.IntegerField(default="1")
	max_usage = models.IntegerField(blank=True, null=True)
	bakers = models.ForeignKey(Baker, blank=True, null=True)
	categories = models.ForeignKey(Category, blank=True, null=True)
	products = models.ForeignKey(Product, blank=True, null=True)


	def __unicode__(self):
   		return self.coupon_code