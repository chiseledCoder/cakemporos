from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, EggVariations, WeightVariations
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponseRedirect
from . import forms
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Avg
from catalog.models import *
from django.http import JsonResponse
# Create your views here.



def product_detail(request, slug):
	user = request.user
	if user.is_active == False:
		logout(request)
	product = get_object_or_404(Product, slug=slug)
	egg_variation = EggVariations.objects.all().filter(product=product)
	weight_variation = WeightVariations.objects.all().filter(product=product)
	box_variation = BoxVariations.objects.all().filter(product=product)
	categories = Category.objects.all()
	site_name = product
	# user_review_exists = ProductReview.objects.filter.exists()
	# if request.method == "POST":
	# 	review_user = request.user
	# 	review_star = request.POST['stars-rating']
	# 	review_content = request.POST['review']
	# 	new_review = ProductReview.objects.create(user=request.user, product=product)
	# 	new_review.rating = review_star
	# 	new_review.content = review_content
	# 	new_review.save()
	# 	messages.success(request, "Your review was submitted!")
	# 	return HttpResponseRedirect(reverse("userindex"))
	# recent_reviews = ProductReview.objects.all().filter(product=product, is_approved=True).order_by('-timestamp')[:10]
	# all_reviews = ProductReview.objects.all().filter(product=product, is_approved=True).order_by('-timestamp')
	# avg_rating = ProductReview.objects.all().filter(product=product, is_approved=True).aggregate(Avg('rating'))
	cakes = Category.objects.filter(title="Cake")
	cupcakes = Category.objects.filter(title="Cupcake")
	# rolls = title.objects.filter(title="Rolls")
	# rusk = title.objects.filter(title="Rusk")
	# bread= title.objects.filter(title="Bread")
	product_cakes = Product.objects.all().filter(slug=slug,title=cakes)
	product_cupcakes = Product.objects.all().filter(slug=slug,title=cupcakes)
	# product_rusk = Product.objects.all().filter(slug=slug,category=rusk)
	# product_rolls = Product.objects.all().filter(slug=slug,category=rolls)
	# product_bread = Product.objects.all().filter(slug=slug,category=bread)
	context = {
		"product" : product,
		"categories" : categories,
		"product_cupcakes":product_cupcakes,
		"site_name": site_name,
		"product_cakes":product_cakes,
		# "recent_reviews": recent_reviews,
		# "all_reviews": all_reviews,
		# "avg_rating":avg_rating,
		
  #   	"product_rolls":product_rolls,
  #   	"product_rusk":product_rusk,
		
  #   	"product_bread":product_bread,
  		"egg_variation": egg_variation,
  		"weight_variation":weight_variation,
  		"box_variation": box_variation
	}
	return render(request, 'products/single.html', context)


def product_like(request, id):
	get_product = get_object_or_404(Product, id=id)
	rating_status = {}
	if request.is_ajax:
		if request.user in get_product.user.all():
			get_product.rating_count -= 1
			get_product.user.remove(request.user)
			get_product.save()
			rating_status['Removed'] = "True"
			rating_status['count'] = get_product.rating_count
			return HttpResponse(JsonResponse(rating_status))
		else:
			get_product.rating_count += 1
			get_product.user.add(request.user)
			get_product.save()
			rating_status['Success'] =  "True"
			rating_status['count'] = get_product.rating_count
			return HttpResponse(JsonResponse(rating_status))
	else:
		rating_status['Success'] =  "False"
		return HttpResponse(JsonResponse(rating_status))
	return request
