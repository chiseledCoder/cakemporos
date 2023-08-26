import json
from django.shortcuts import render, HttpResponseRedirect, render_to_response, HttpResponse, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout
from catalog.models import *
from django.utils.datastructures import MultiValueDictKeyError
from catalog.models import Product, Addon
from .models import Cart, CartItem
from django.http import JsonResponse
from core.models import Locality
# Create your views here.

def update_cart(request, id):
	user = request.user
	if user.is_active == False:
		logout(request)
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
	quick_update = {}
	if request.method == "POST":

		if 'boxes' not in request.POST:
			boxes = 0
		else:
			boxes = request.POST['boxes']

		if 'egg_or_eggless' not in request.POST:
			egg_or_eggless = 0
		else:
			egg_or_eggless = request.POST['egg_or_eggless']

		if 'msg_on_cake' not in request.POST:
			msg_on_cake = "No Msg On cake"
		else:
			msg_on_cake = request.POST['msg_on_cake']

		if 'weight' not in request.POST:
			weight = 0
		else:
			weight = request.POST['weight']

		if 'photo_cake_file' not in request.FILES:
			photo_cake_file = None
		else:
			photo_cake_file = request.FILES['photo_cake_file']

		if 'qty' not in request.POST:
			qty = 1
		else:
			qty = request.POST['qty']

		update_cart_item = get_object_or_404(CartItem, cart=cart, id=id)
		product = update_cart_item.product 
		update_cart_item.msg_on_cake = msg_on_cake
		update_cart_item.quantity = qty
		update_cart_item.photo_cake_image = photo_cake_file

		if egg_or_eggless == 0:
			pass
		else:
			egg_variant = EggVariations.objects.get(product=product, egg_variation_type=egg_or_eggless)
			update_cart_item.egg_or_eggless = egg_variant
			update_cart_item.egg_or_eggless_price = egg_variant.extra_price
	
		if weight == 0:
			pass
		else:
			weight_variant = WeightVariations.objects.get(product=product, weight_variation_type=weight)
			update_cart_item.weight = weight_variant
			update_cart_item.weight_price = weight_variant.price

		if boxes == 0:
			pass
		else:
			box_variant = BoxVariations.objects.get(product=product, box_variation_type=boxes)
			update_cart_item.cupcake_qty = box_variant
			update_cart_item.cupcake_qty_price = box_variant.price

		update_cart_item.save()
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =( (float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty)
			item.save()
			new_total += line_total
			if item.product == update_cart_item.product:
				update_line_total = ((float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty) + (float(item.giftitem_price) * item.giftitem_qty)
				item.cart_item_total = update_line_total
				update_cart_item.cart_item_total = update_line_total
				update_cart_item.save()
			else:
				pass
		cart.total = new_total
		cart.coupon = None
		cart.save()
		update_cart_item.save()
		return HttpResponseRedirect(reverse("checkout"))
	return HttpResponseRedirect(reverse("cart"))


def view_cart(request):
	user = request.user
	if user.is_active == False:
		logout(request)
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
	if the_id:
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =( (float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty)
			item.cart_item_total = line_total
			item.save()
			new_total += line_total
		request.session['items_total'] = cart.cartitem_set.count()
		total_items = cart.cartitem_set.count()
		if total_items == "0":
			empty_message = "Your Cart is Empty, please keep shopping."
			context = {
				"empty": True,
				"empty_message": empty_message,
				"site_name":"Cart"
				}
		cart.total = new_total
		cart.coupon = None
		cart.save()
		context = {
			"cart": cart,
			"site_name":"Cart"
			}
	else:
		empty_message = "Your Cart is Empty, please keep shopping."
		context = {
			"empty": True,
			"empty_message": empty_message,
			"site_name":"Cart"
		}
	template = "cart/cart_view.html"
	return render(request, template, context)


def remove_from_cart(request, id):
	user = request.user
	if user.is_active == False:
		logout(request)
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse("cart"))
	cartitem = CartItem.objects.get(id=id)
	#cartitem.delete()
	cartitem.cart = None
	cartitem.save()
	cart.coupon = None
	cart.save()
	#send "success message"
	return HttpResponseRedirect(reverse("cart"))
		



def add_to_cart(request, slug):
	request.session.set_expiry(120000)
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)
	cart.coupon = None
	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass
	product_var = []
	if request.method == "POST":
		if 'boxes' not in request.POST:
		    boxes = 0
		else:
		    boxes = request.POST['boxes']

		if 'egg_or_eggless' not in request.POST:
		    egg_or_eggless = 0
		else:
		    egg_or_eggless = request.POST['egg_or_eggless']

		delivery_date = request.POST['delivery_date']
		delivery_time = request.POST['deleivery_time']
		
		if 'msg_on_cake' not in request.POST:
		    msg_on_cake = 0
		else:
		    msg_on_cake = request.POST['msg_on_cake']

		if 'weight' not in request.POST:
		    weight = 0
		else:
		    weight = request.POST['weight']

		if 'qty' not in request.POST:
		    qty = 1
		else:
		    qty = request.POST['qty']


		if 'photo_cake_file' not in request.FILES:
			photo_cake_file = None
		else:
			photo_cake_file = request.FILES['photo_cake_file']

		cart_item = CartItem.objects.create(cart=cart, product=product)
	
		if egg_or_eggless == 0:
			pass
		else:
			egg_variant = EggVariations.objects.get(product=product, egg_variation_type=egg_or_eggless)
			cart_item.egg_or_eggless = egg_variant
			cart_item.egg_or_eggless_price = egg_variant.extra_price
	
		if weight == 0:
			pass
		else:
			weight_variant = WeightVariations.objects.get(product=product, weight_variation_type=weight)
			cart_item.weight = weight_variant
			cart_item.weight_price = weight_variant.price

		if boxes == 0:
			pass
		else:
			box_variant = BoxVariations.objects.get(product=product, box_variation_type=boxes)
			cart_item.cupcake_qty = box_variant
			cart_item.cupcake_qty_price = box_variant.price
		
		cart_item.delivery_date = delivery_date
		cart_item.delivery_time = delivery_time
		cart_item.msg_on_cake = msg_on_cake
		cart_item.quantity = qty
		cart_item.photo_cake_image = photo_cake_file
		if cart_item.photo_cake_image:
			photocustomization = PhotoCakeCustomization.objects.get(baker=product.baker, weight=cart_item.weight)
			cart_item.photo_cake_cost = photocustomization.price
		cart_item.save()
		return HttpResponseRedirect(reverse("cart"))
	return HttpResponseRedirect(reverse("cart"))


def quick_add_to_cart(request, slug):
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)
	cart.coupon = None
	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass

	quick_cart = {}
	if request.method == "POST" and request.is_ajax:
		cart_item = CartItem.objects.create(cart=cart, product=product)

		if 'boxes' not in request.POST:
		    boxes = 0
		else:
		    boxes = request.POST['boxes']

		if 'egg_or_eggless' not in request.POST:
		    egg_or_eggless = 0
		else:
		    egg_or_eggless = request.POST['egg_or_eggless']

		if 'weight' not in request.POST:
		    weight = 0
		else:
		    weight = request.POST['weight']
		
		if egg_or_eggless == 0:
			pass
		else:
			egg_variant = EggVariations.objects.get(product=product, egg_variation_type=egg_or_eggless)
			cart_item.egg_or_eggless = egg_variant
			cart_item.egg_or_eggless_price = egg_variant.extra_price
	
		if weight == 0:
			pass
		else:
			weight_variant = WeightVariations.objects.get(product=product, weight_variation_type=weight)
			cart_item.weight = weight_variant
			cart_item.weight_price = weight_variant.price

		if boxes == 0:
			pass
		else:
			box_variant = BoxVariations.objects.get(product=product, box_variation_type=boxes)
			cart_item.cupcake_qty = box_variant
			cart_item.cupcake_qty_price = box_variant.price

		cart_item.save()
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =( (float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty)
			item.cart_item_total = line_total
			item.save()
			cart_product = item.product
			new_total += line_total

		locality_id = request.session['locality_id']

		cart_weight = 0
		half_kg = 0.5
		one_kg = 1
		one_and_half_kg = 1.5
		two_kg = 2


		cart.locality = get_object_or_404(Locality, id=locality_id)
		cart.sub_total = new_total
		cart.coupon = None
		cart.save()
		quick_cart['get_total_items_count'] = CartItem.objects.filter(cart=cart).count()
		quick_cart['get_cart_item_total'] = line_total
		quick_cart['get_cart_id'] = cart_item.id
		quick_cart['get_cart_total'] =  cart.sub_total
		quick_cart['get_cart_item'] = cart_item.product.title
		quick_cart['get_cart_item_slug'] = cart_item.product.slug
		quick_cart['get_cart_item_id'] = cart_item.product.id
		quick_cart['get_cart_item_baker'] = cart_item.product.baker.shop_name
		
		return HttpResponse(JsonResponse(quick_cart))
	return HttpResponseRedirect(reverse("cart"))



def quick_update_cart(request, slug):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
	product = get_object_or_404(Product, slug=slug)
	quick_update = {}
	if request.method == "POST" and request.is_ajax:

		if 'boxes' not in request.POST:
			boxes = 0
		else:
			boxes = request.POST['boxes']

		if 'egg_or_eggless' not in request.POST:
			egg_or_eggless = 0
		else:
			egg_or_eggless = request.POST['egg_or_eggless']

		if 'msg_on_cake' not in request.POST:
			msg_on_cake = "No Msg On cake"
		else:
			msg_on_cake = request.POST['msg_on_cake']

		if 'weight' not in request.POST:
			weight = 0
		else:
			weight = request.POST['weight']

		if 'photo_cake_file' not in request.FILES:
			photo_cake_file = None
		else:
			photo_cake_file = request.FILES['photo_cake_file']

		if 'qty' not in request.POST:
			qty = 1
		else:
			qty = request.POST['qty']

		if 'comment' not in request.POST:
			comment = 1
		else:
			comment = request.POST['comment']

		update_cart_item = get_object_or_404(CartItem, cart=cart, product=product)
		update_cart_item.msg_on_cake = msg_on_cake
		update_cart_item.quantity = qty
		update_cart_item.notes = comment
		update_cart_item.photo_cake_image = photo_cake_file

		if egg_or_eggless == 0:
			pass
		else:
			egg_variant = EggVariations.objects.get(product=product, egg_variation_type=egg_or_eggless)
			update_cart_item.egg_or_eggless = egg_variant
			update_cart_item.egg_or_eggless_price = egg_variant.extra_price
	
		if weight == 0:
			pass
		else:
			weight_variant = WeightVariations.objects.get(product=product, weight_variation_type=weight)
			update_cart_item.weight = weight_variant
			update_cart_item.weight_price = weight_variant.price

		if boxes == 0:
			pass
		else:
			box_variant = BoxVariations.objects.get(product=product, box_variation_type=boxes)
			update_cart_item.cupcake_qty = box_variant
			update_cart_item.cupcake_qty_price = box_variant.price

		update_cart_item.save()
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =( (float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty)
			item.save()
			new_total += line_total
			if item.product == update_cart_item.product:
				update_line(_total = (float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty)
				item.cart_item_total = update_line_total
				update_cart_item.cart_item_total = update_line_total
				update_cart_item.save()
			else:
				pass
		cart.sub_total = new_total
		cart.coupon = None
		cart.save()
		update_cart_item.save()
		quick_update['get_cart_total'] = cart.sub_total
		quick_update['get_cart_item'] = update_cart_item.product.title
		quick_update['get_cart_item_id'] = update_cart_item.id
		quick_update['get_cart_item_qty'] = update_cart_item.quantity
		quick_update['get_cart_item_egg'] = update_cart_item.egg_or_eggless.egg_variation_type
		quick_update['get_cart_item_egg_price'] = update_cart_item.egg_or_eggless_price
		quick_update['get_cart_item_weight'] = update_cart_item.weight.weight_variation_type
		quick_update['get_cart_item_weight_price'] = update_cart_item.weight_price
		quick_update['get_cart_item_msg_on_cake'] = update_cart_item.msg_on_cake
		# quick_update['get_cart_item_photo_cake_image'] = update_cart_item.photo_cake_image
		quick_update['get_cart_item_photo_cake_cost'] = update_cart_item.photo_cake_cost
		quick_update['get_cart_item_total']= update_cart_item.cart_item_total
		return HttpResponse(JsonResponse(quick_update))
	return HttpResponseRedirect(reverse("cart"))

def quick_remove_from_cart(request, id):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse("cart"))
	quick_remove={}
	if request.is_ajax:
		cart_item = CartItem.objects.get(cart=cart, id=id)
		if cart_item.product:
			quick_remove['get_cart_item_id'] = cart_item.product.id
		elif cart_item.addon:
			quick_remove['get_cart_item_id'] = cart_item.addon.id
		elif cart_item.giftitem:
			quick_remove['get_cart_item_id'] = cart_item.giftitem.id
		cart_item.delete()
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total = ((float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty) + (float(item.giftitem_price) * item.giftitem_qty)
			item.cart_item_total = line_total
			item.save()
			if item.product:
				cart_product = item.product
			elif item.addon:
				cart_product = item.addon
			new_total += line_total
		cart.sub_total = new_total
		cart.coupon = None
		cart.save()
		quick_remove['get_total_items_count'] = CartItem.objects.filter(cart=cart).count()
		quick_remove['get_cart_total'] =  cart.sub_total
		return HttpResponse(JsonResponse(quick_remove))
	return HttpResponse(JsonResponse(quick_remove))



def quick_addon(request):
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)
	cart.coupon = None

	

	quick_addon = {}
	if request.method == "POST":
			
		form_addons = request.POST.getlist('addons')
		for item in form_addons:
			try:
				addon = Addon.objects.get(slug=item)
			except Addon.DoesNotExist:
				pass
			except:
				pass
			cart_item = CartItem.objects.create(cart=cart, addon=addon)
			cart_item.addon_price = addon.price
			cart_item.save()
		
		
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =((float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty) + (float(item.giftitem_price) * item.giftitem_qty)
			item.cart_item_total = line_total
			item.save()
			cart_product = item.product
			new_total += line_total

		cart.sub_total = new_total
		cart.coupon = None
		cart.save()

		quick_addon['get_total_items_count'] = CartItem.objects.filter(cart=cart).count()
		quick_addon['get_cart_item_total'] = line_total
		quick_addon['get_cart_id'] = cart_item.id
		quick_addon['get_cart_total'] =  cart.sub_total
		return HttpResponseRedirect(reverse("checkout"))
	return HttpResponseRedirect(reverse("checkout"))

def quick_addon(request):
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)
	cart.coupon = None

	

	quick_addon = {}
	if request.method == "POST":
			
		form_addons = request.POST.getlist('addons')
		for item in form_addons:
			try:
				addon = Addon.objects.get(slug=item)
			except Addon.DoesNotExist:
				pass
			except:
				pass
			cart_item = CartItem.objects.create(cart=cart, addon=addon)
			cart_item.addon_price = addon.price
			cart_item.save()
		
		
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =((float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty) + (float(item.giftitem_price) * item.giftitem_qty)
			item.cart_item_total = line_total
			item.save()
			cart_product = item.product
			new_total += line_total

		cart.sub_total = new_total
		cart.coupon = None
		cart.save()

		quick_addon['get_total_items_count'] = CartItem.objects.filter(cart=cart).count()
		quick_addon['get_cart_item_total'] = line_total
		quick_addon['get_cart_id'] = cart_item.id
		quick_addon['get_cart_total'] =  cart.sub_total
		return HttpResponseRedirect(reverse("checkout"))
	return HttpResponseRedirect(reverse("checkout"))


def quick_giftitem_addtocart(request, id):
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)
	cart.coupon = None	

	quick_giftitem = {}
	try:
		giftitem = GiftItem.objects.get(id=id)
	except GiftItem.DoesNotExist:
		giftitem = None

	if giftitem is not None:
		cart_item = CartItem.objects.create(cart=cart, giftitem=giftitem)
		cart_item.giftitem_price = giftitem.price
		cart_item.save()
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total =((float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty) + (float(item.giftitem_price) * item.giftitem_qty)
			item.cart_item_total = line_total
			item.save()
			cart_product = item.product
			new_total += line_total

		cart.sub_total = new_total
		cart.coupon = None
		cart.save()

		quick_giftitem['get_total_items_count'] = CartItem.objects.filter(cart=cart).count()
		quick_giftitem['get_cart_item_total'] = line_total
		quick_giftitem['get_cart_id'] = cart_item.id
		quick_giftitem['get_cart_total'] =  cart.sub_total	

		return HttpResponseRedirect(reverse("checkout"))
	return HttpResponseRedirect(reverse("checkout"))