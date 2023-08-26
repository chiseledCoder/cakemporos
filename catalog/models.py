from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from bakers.models import Baker
from giftsellers.models import GiftSeller
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import format_html
# from autoslug import AutoSlugField

STATUS = (
		("Enabled", "Enabled"),
		("Disabled", "Disabled"),
	)
PRODUCTS_VEGEN = (
		("Both", "Both"),
		("Only Vegeterian", "Only Vegeterian"),
		("Only Non-Vegeterian", "Only Non-Vegeterian"),
	)
CAKE_SHAPE = (
	("Round","Round"),
	("Square or Rectangular","Square or Rectangular")
	)
EGG_VARIATION = (
	("Egg","Egg"),
	("Eggless","Eggless")
	)
WEIGHT_VARIATION = (
	("0.5 Kg"," 0.5 Kg"),
	("1 Kg","1 Kg"),
	("1.5 Kg"," 1.5 Kg"),
	("2 Kg","2 Kg")
	)
 
BOX_VARIATION = (
	("1 Box","1 Box"),
	("2 Box","2 Box"),
	("3 Box","3 Box"),
	("4 Box","4 Box"),
	("5 Box","5 Box"),
	("6 Box","6 Box"),
	)
#Create your models here.
class ProductType(models.Model):
	title = models.CharField(max_length=100, null=True, blank=True)
	def __unicode__(self):
		return self.title

class Category(models.Model):
	"""docstring for ClassName"""
	title = models.CharField(max_length=100, null=True, blank=True)

	def __unicode__(self):
		return self.title

class Product(models.Model):
	baker = models.ForeignKey(Baker, null=True, blank=True)
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey('Category', null=True, blank=True)
	product_type = models.ForeignKey('ProductType', null=True, blank=True)
	#subcategory = models.ManyToManyField('SubCategory', null=True, blank=True)
	featured = models.BooleanField(default=False)
	image = models.ImageField(upload_to='products/images/', default="products/default.jpg")
	veg_or_nonveg = models.CharField(max_length=100, choices=PRODUCTS_VEGEN, default="Both")
	status = models.CharField(max_length=100, choices=STATUS, default="Disabled")
	user = models.ManyToManyField(User, blank=True)
	rating_count = models.IntegerField(default=0)
	slug = models.SlugField(max_length=200, unique=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = '-'.join((slugify(self.baker), slugify(self.title)))
		super(Product, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('product_detail', kwargs={"slug": self.slug})

	def get_absolute_image_url(self):
		return '%s%s' % (settings.S3_URL, self.image.url)

	def get_image(self):
		return format_html('<img src="%s/%s" height="100" width="100"/>' % (settings.S3_URL, self.image))

		image_tag.short_description = 'Image'

class PhotoCakeCustomization(models.Model):
	baker = models.ForeignKey(Baker, default="")
	weight = models.CharField(choices=WEIGHT_VARIATION, default="0.5 Kg", max_length=100)
	price = models.DecimalField(decimal_places=2, max_digits=10)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.weight

class CakeCustomization(models.Model):
	baker = models.ForeignKey(Baker, default="")
	starting_weight = models.CharField(choices=WEIGHT_VARIATION, default="0.5 Kg", max_length=100)
	starting_price = models.DecimalField(decimal_places=2, max_digits=10)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.starting_weight

class EggVariations(models.Model):
	product = models.ForeignKey(Product, default="", null=True, blank=True)
	egg_variation_type = models.CharField(max_length=100, choices=EGG_VARIATION, default="Eggless")
	extra_price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.egg_variation_type

class WeightVariations(models.Model):
	product = models.ForeignKey(Product, default="", null=True, blank=True)
	weight_variation_type = models.CharField(max_length=100, choices=WEIGHT_VARIATION, default="0.5 Kg")
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.weight_variation_type
		
class BoxVariations(models.Model):
	product = models.ForeignKey(Product, default="", null=True, blank=True)	
	box_variation_type = models.CharField(max_length=100, choices=BOX_VARIATION, default="1 Box")
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.box_variation_type

class CakeOfTheDay(models.Model):
	"""docstring for CakeOfTheDay"""
	cake = models.ForeignKey(Product, default="", null=True, blank=True)	
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name_plural = 'Cake of the Day'

	def __unicode__(self):
		return "Cake of the Day: %s (%s) " %(self.cake, self.cake.baker)


class Addon(models.Model):
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to='addons/images/', default="products/default.jpg")
	slug = models.SlugField(max_length=200, unique=True, null=True)
	price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	status = models.BooleanField(default=False)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = '-'.join(("Addon", slugify(self.title), str(self.id)))
		super(Addon, self).save(*args, **kwargs)

	def get_image(self):
		return format_html('<img src="%s/%s" height="100" width="100"/>' % (settings.S3_URL, self.image))

		image_tag.short_description = 'Image'

class GiftItem(models.Model):
	brand = models.ForeignKey(GiftSeller)
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to='addons/images/', default="products/default.jpg")
	slug = models.SlugField(max_length=200, unique=True, null=True)
	price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	status = models.BooleanField(default=False)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = '-'.join(("GiftItem", slugify(self.title), str(self.id)))
		super(GiftItem, self).save(*args, **kwargs)

	def get_image(self):
		return format_html('<img src="%s/%s" height="100" width="100"/>' % (settings.S3_URL, self.image))

		image_tag.short_description = 'Image'