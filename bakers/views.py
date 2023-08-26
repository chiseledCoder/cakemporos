from django.shortcuts import render
from bakers.models import Locality, Sub_Locality, Baker
from catalog.models import *
from cart.models import *
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from random import shuffle
# Create your views here.

def locality_search(request):
	user = request.user
	if user.is_authenticated == True and user.is_active == False:
		logout(request)
	try:
		locality_search = request.GET.get('q')
	except:
		locality_search = None
	
	if locality_search:
		locality_name = Locality.objects.get(locality_name=locality_search)
		request.session['locality_id'] = locality_name.id
		"""Add user locality"""
		try:
			the_id = request.session['cart_id']
			cart = Cart.objects.get(id=the_id)
			if the_id:
				if cart.locality == locality_name:
					pass
				else:
					for item in cart.cartitem_set.all():
						item.delete()
		except:
			cart = None
			error = "Passing"
			context = {
			"error" : error
			}
			pass

		get_all_locality = Locality.objects.get(locality_name="All")
		baker_locality = Baker.objects.filter(serving_localities=locality_name)
		get_all_baker = Baker.objects.all().filter(serving_localities=get_all_locality)
		baker_products = list(Product.objects.filter(Q(baker__in=baker_locality) | Q(baker__in=get_all_baker), status="Enabled"))
		shuffle(baker_products)
		cartitem = CartItem.objects.filter(cart=cart)
		cartitem_product = [item.product for item in cartitem]
		site_name = locality_name
		context = {
			"query": locality_search,
			"baker_locality": baker_locality,
			"baker_products": baker_products,
			"cartitem":cartitem,
			"cartitem_product":cartitem_product,
			"site_name": site_name
			}
		template = 'bakers/results.html'	
		return render(request, template, context)
	else:
		template = 'index.html'
		return render(request, template)