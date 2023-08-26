from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sales.models import Coupon
from datetime import date
from core.models import Locality
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")

# Create your models here.

class UserAccount(models.Model):
	user = models.OneToOneField(User, related_name='userprofile')
	is_corporate = models.BooleanField(default=False, blank=True)
	is_cakemporos_baker = models.BooleanField(default=False, blank=True)
	is_first_time_user = models.BooleanField(default=False, blank=True)
	phone = models.CharField(validators=[phone_regex], blank=False, max_length=20, unique=True)
	user_locality = models.ForeignKey(Locality, blank=True, null=True)
	user_otp = models.IntegerField(blank=True, null=True)
	user_otp_session = models.CharField(max_length=100, blank=True, null=True)
	coupon = models.ManyToManyField(Coupon, default="", blank=True)
	reward_id = models.CharField(max_length=120, default='ABC', unique=True)
	access_token = models.CharField(max_length=100, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.phone

	class Meta:
		verbose_name_plural = 'User Accounts'
		app_label = 'accounts'		##To supress django 1.9 app label error 
		unique_together = ("id", "phone", "reward_id")

	def coupons_list(self):
		return ",\n".join([s.coupon_code for s in self.coupon.all()])

class UserAddresses(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	user_addresses = models.TextField()
	user_locality = models.TextField(default="")
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.user_addresses

	class Meta:
		verbose_name_plural = "User's Shipping Addresses"
		app_label = 'accounts'