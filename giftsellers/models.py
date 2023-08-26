from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

STATUS = (
		("Enabled", "Enabled"),
		("Disabled", "Disabled"),
	)
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
	
class GiftSeller(models.Model):
	owner = models.CharField(max_length=150)
	description = models.TextField(default='', max_length=250)
	shop_name = models.CharField(default='', max_length=50)
	shop_pno = models.CharField(validators=[phone_regex], blank=True, max_length=13)
	shop_address = models.TextField(default='', max_length=250)
	image = models.ImageField(upload_to='giftseller/images/', default="giftseller/default.jpg")
	GST_number = models.CharField(max_length=500, default="", blank=True)
	mou_signed_on = models.DateField('Date', default=timezone.now)
	featured = models.BooleanField(default=False)
	status = models.CharField(max_length=100, choices=STATUS, default="Disabled")
	slug = models.SlugField(unique=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	class Meta:
		ordering = ["-timestamp"]

	def __unicode__(self):
		return self.shop_name

	def save(self, *args, **kwargs):
		self.slug = '-'.join((slugify(self.shop_name), slugify(self.owner)))
		super(GiftSeller, self).save(*args, **kwargs)