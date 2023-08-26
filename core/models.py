from django.db import models
from django.conf import settings
import random
from django.utils import timezone
from django.utils.html import format_html
# Create your models here.


class Locality(models.Model):
	locality_name = models.CharField(max_length=50, null=False, blank=False)
	pincode = models.IntegerField(default=400001, null=False, blank=False)
	status = models.BooleanField(default=False)
	timestamp = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		ordering = ["locality_name"]

	def __unicode__(self):
		return self.locality_name

class Sub_Locality(models.Model):
	locality = models.ForeignKey(Locality, blank=False, null=False)
	sub_locality = models.CharField(max_length=100, null=False, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		ordering = ["locality"]
	def __unicode__(self):
		return self.sub_locality

class About(models.Model):
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name_plural = 'About Us'

	def __unicode__(self):
		return str("About Us")

class Terms(models.Model):
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name_plural = 'Terms & Conditions'

	def __unicode__(self):
		return str("Terms & Conditions")

class Privacy(models.Model):
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name_plural = 'Privacy Policy'

	def __unicode__(self):
		return str("Privacy Policy")

class FAQ(models.Model):
	question = models.CharField(max_length=100)
	answer = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name_plural = 'Frequently Asked Questions'

	def __unicode__(self):
		return self.question


class Offers(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	coupon_code = models.CharField(max_length=100)
	image = models.ImageField(upload_to='offers/images/', default="baker/default.jpg")
	status = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name_plural = 'Offers'

	def __unicode__(self):
		return self.title

	def get_image(self):
		return format_html('<img src="%s/%s" height="100" width="100"/>' % (settings.S3_URL, self.image))

		image_tag.short_description = 'Image'