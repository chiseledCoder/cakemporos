import time
import json
from decimal import Decimal
from django.shortcuts import render, HttpResponseRedirect, render_to_response, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import timezone
from django.utils.timezone import datetime, timedelta
from django.core.exceptions import PermissionDenied
from accounts.models import *
from bakers.models import *
from cart.models import *
from catalog.models import *
from order.models import *

# Create your views here.

def applycoupon(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
		cart.coupon = None
	except:
		the_id = None
		return HttpResponseRedirect(reverse("/checkout"))
	if request.method == "POST" and request.is_ajax:
		user = request.user
		useraccount = UserAccount.objects.get(user=user)
		coupon_code = request.POST['couponcode']
		updated_cart = {}
		try:
			code = Coupon.objects.get(coupon_code__iexact=coupon_code, active=True, start_date__lte=timezone.now(), expiry_date__gte=timezone.now())
			if code.usage_per_person == 1 and code in useraccount.coupon.all():
				updated_cart['failed'] = "False"
				return HttpResponse(json.dumps(updated_cart))
			else:
				cart.sub_total = cart.sub_total - code.coupon_cost
				cart.coupon = code
				cart.service_charge_value = (cart.sub_total * 0)/100
				cart.total = cart.sub_total + cart.service_charge_value
				cart.save()
				updated_cart['coupon'] = coupon_code
				updated_cart['coupon_cost'] = code.coupon_cost
				updated_cart['sub_total'] = float(cart.sub_total)
				updated_cart['total'] = float(cart.total)
				updated_cart['service_charge'] = float(cart.service_charge_value)

				return HttpResponse(json.dumps(updated_cart))
		except Coupon.DoesNotExist:
			updated_cart['failed'] = "False"
			return HttpResponse(json.dumps(updated_cart))
	return HttpResponseRedirect(reverse("checkout"))

