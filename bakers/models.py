from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.contrib.auth.models import User
from core.models import *
# Create your models here.
BAKER_TYPE = (
		("Home", "Home"),
		("Local", "Local"),
	)
STATUS = (
		("Enabled", "Enabled"),
		("Disabled", "Disabled"),
	)
AVAILABLE_VEGEN = (
		("Both", "Both"),
		("Only Vegeterian", "Only Vegeterian"),
		("Only Non-Vegeterian", "Only Non-Vegeterian"),
	)
MIN_WEIGHT = (
		("0.5 Kg and above","0.5 Kg and above"),
		("1 Kg and above","1 Kg and above"),
		("1.5 Kg and above","1.5 Kg and above"),
	)
MIN_ORDER_TIME =(
		("0-3 Hrs","0-3 Hrs"),
		("3-6 Hrs","3-6 Hrs"),
		("6-9Hrs","6-9Hrs"),
		("Above 12 Hrs","Above 12 Hrs"),
	)
		
class Baker(models.Model):
	owner = models.ForeignKey(User, blank=True, null=True, related_name="baker")
	description = models.TextField(default='', max_length=250)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
	owner_address = models.TextField(default='', max_length=250)
	baker_type = models.CharField(max_length=10, choices=BAKER_TYPE, default="Local")
	shop_name = models.CharField(default='', max_length=50)
	shop_pno = models.CharField(validators=[phone_regex], blank=True, max_length=13)
	shop_address = models.TextField(default='', max_length=250)
	serving_localities = models.ManyToManyField(Locality, default="")
	shop_locality = models.CharField(max_length=200, default="")
	veg_or_nonveg = models.CharField(max_length=100, choices=AVAILABLE_VEGEN, default="Both")
	min_order_time = models.CharField(default="", choices=MIN_ORDER_TIME, max_length=50)
	image = models.ImageField(upload_to='baker/images/', default="baker/default.jpg")
	shop_license_number = models.CharField(max_length=500, default="", blank=True)
	mou_signed_on = models.DateField('Date')
	featured = models.BooleanField(default=False)
	status = models.CharField(max_length=100, choices=STATUS, default="Disabled")
	customized_cake_option = models.BooleanField(default=False)
	photo_cake_option = models.BooleanField(default=False)
	min_weight_for_customization = models.CharField(max_length=200, choices=MIN_WEIGHT, default="0.5 and above")
	min_weight_for_photocake = models.CharField(max_length=200, choices=MIN_WEIGHT, default="0.5 and above")
	slug = models.SlugField(unique=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	class Meta:
		ordering = ["-timestamp"]

	def __unicode__(self):
		return self.shop_name

	def save(self, *args, **kwargs):
		self.slug = '-'.join((slugify(self.shop_name), slugify(self.owner.get_full_name())))
		super(Baker, self).save(*args, **kwargs)

	# def get_absolute_url(self):
	# 	return reverse('baker_detail', kwargs={"slug": self.slug})

	def serving_locality_list(self):
		return ",\n".join([item.locality_name for item in self.serving_localities.all()])