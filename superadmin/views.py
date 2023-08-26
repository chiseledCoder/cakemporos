from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from .forms import SuperAdminLoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView
from bakers.models import *
from order.models import *
# Create your views here.

def superadmin_logout_view(request):
	logout(request)
	return HttpResponseRedirect('%s'%(reverse("superadmin_login")))

def superadmin_login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/superadmin/dashboard")

	form = SuperAdminLoginForm(request.POST or None)
	btn = "Login"

	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		messages.success(request, "Successfully Logged In. Welcome Back!")
		return HttpResponseRedirect("/superadmin/dashboard")
	context = {
		"form": form,
		"submit_btn": btn,
	}
	return render(request, "superadmin/login.html", context)


@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_dashboard(request):
	context = {
		"site_title": "Dashboard"
	}
	template = "superadmin/ce_dash.html"
	return render(request, template, context)

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_bakers_list(request):
	template = "superadmin/baker/superadmin_bakers_list.html"
	context = {
		"site_title": "Bakers List"
	}
	return render(request, template, context)

class BakersListJSON(BaseDatatableView):

	model = Baker
	columns = ['shop_name',  'owner', 'address', 'shop_pno', 'baker_type', 'veg_or_nonveg', 'status', 'action']
	order_columns =  ['shop_name', 'owner']
	max_display_length = 500
	def render_column(self, row, column):
		if column == 'shop_name':
			return row.shop_name
		elif column == 'owner':
			return '%s' %(row.owner.get_full_name())
		elif column == 'address':
			return row.shop_address
		elif column == 'shop_pno':
			get_useraccount = UserAccount.objects.get(user=row.owner)
			return get_useraccount.phone
		elif column == 'baker_type':
			return row.baker_type
		elif column == 'veg_or_nonveg':
			return row.veg_or_nonveg
		elif column == 'status':
			if row.status == "Enabled":
				return '<span class="badge badge-success"><i class="fa fa-check"></span>'
			elif row.status == "Disabled":
				return '<span class="badge badge-danger"><i class="fa fa-times"></span>'
		elif column == 'action':
			baker_detail_url = reverse('superadmin_baker_details', args=(row.slug,))
			return '<a href="%s">Update</a>' %baker_detail_url
		else:
			return super(BakersListJSON, self).render_column(row, column)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(BakersListJSON, self).dispatch(request, *args, **kwargs)

def superadmin_baker_details(request, slug):
	baker = get_object_or_404(Baker, slug=slug)
	bakers_products = Product.objects.filter(baker=baker)
	total_products = bakers_products.count()
	bakers_orders = Order.objects.filter(baker=baker)
	recent_bakers_orders = Order.objects.filter(baker=baker, approve=True)[:5]
	total_orders = bakers_orders.count()
	sales_last_seven_days = Order.objects.filter(baker=baker, approve=True).values('order_date').annotate(total=Sum('final_total'))
	total_sales_last_seven_days = list(sales_last_seven_days)
	total_sales = 0
	for item in sales_last_seven_days:
		total_sales += item['total']
	template = "superadmin/baker/superadmin_baker_details.html"
	context = {
		"site_title": "Baker's Details",
		"baker": baker,
		"total_products": total_products,
		"total_orders": total_orders,
		"recent_bakers_orders": recent_bakers_orders,
		"total_sales": total_sales
	}
	return render(request, template, context)

class ProductsListByBakerJson(BaseDatatableView):
	columns = ['title', 'category', 'product_type', 'image', 'veg_or_nonveg', ]
	order_columns = ['title', 'category', 'product_type']
	max_display_length = 500

	def get_initial_queryset(self):
		baker = get_object_or_404(Baker, slug=self.kwargs['slug'])
		return Product.objects.all().filter(baker=baker)

	def prepare_results(self, qs):
		# prepare list with output column data
		# queryset is already paginated here
		json_data = []
		for item in qs:
			if item.status == "Enabled":
				status = '<span class="label label-success">'+item.status+'</span>'
			else:
				status = '<span class="label label-danger">'+item.status+'</span>'
			json_data.append([
				item.title,
				'%s' %(item.product_type),
				'%s' %(item.category),
				item.get_image(),
				item.veg_or_nonveg,
				status,
				])
		return json_data

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(ProductsListByBakerJson, self).dispatch(request, *args, **kwargs)

class OrdersListByBakerJson(BaseDatatableView):
	columns = ['order_title', 'user', 'cart', 'cartitem', 'status', 'approve', 'payment_clearance', 'final_total' ]
	order_columns = ['order_title', 'cart', 'cartitem', 'status']
	max_display_length = 500

	def get_initial_queryset(self):
		baker = get_object_or_404(Baker, slug=self.kwargs['slug'])
		return Order.objects.all().filter(baker=baker)

	def prepare_results(self, qs):
		# prepare list with output column data
		# queryset is already paginated here
		json_data = []
		for item in qs:
			if item.approve == True:
				approve = '<span class="badge badge-success"><i class="fa fa-check"></span>'
			else:
				approve = '<span class="badge badge-danger"><i class="fa fa-times"></span>'

			if item.payment_clearance == True:
				payment_clearance = '<span class="badge badge-success"><i class="fa fa-check"></span>'
			else:
				payment_clearance = '<span class="badge badge-danger"><i class="fa fa-times"></span>'
			view_more = '<a href="#">View</i>'
			json_data.append([
				item.order_id,
				'%s' %(item.user.get_full_name()),
				'%s' %(item.cartitem),
				'%s' %(item.cartitem.addon),
				item.status,
				approve,
				payment_clearance,
				item.final_total,
				view_more
				])
		return json_data

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(OrdersListByBakerJson, self).dispatch(request, *args, **kwargs)

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_add_new_product(request, slug):
	"""ADD new product to the baker """
	get_baker = get_object_or_404(Baker, slug=slug)
	print get_baker
	categories = Category.objects.all()
	product_types = ProductType.objects.all()
	if request.method == "POST":
		if "product_title" not in request.POST:
			product_title = None
		else:
			product_title = request.POST["product_title"]

		if "product_by_type" not in request.POST:
			product_by_type = 0
		else:
			product_by_type = request.POST["product_by_type"]
		print product_by_type

		if "product_by_category" not in request.POST:
			product_by_category = 0
		else:
			product_by_category = request.POST["product_by_category"]

		if "product_description" not in request.POST:
			product_description = None
		else:
			product_description = request.POST["product_description"]

		if "product_status" not in request.POST:
			product_status = "Disabled"
		else:
			product_status = request.POST["product_status"]

		product_veg_or_nonveg = get_baker.veg_or_nonveg

		if "egg_or_eggless_variant" not in request.POST:
			egg_or_eggless_variant = None
		else:
			egg_or_eggless_variant = request.POST.getlist("egg_or_eggless_variant")

		if "egg_or_eggless_price" not in request.POST:
			egg_or_eggless_price = 0
		else:
			egg_or_eggless_price = request.POST["egg_or_eggless_price"]

		if "eggless_price" not in request.POST:
			eggless_price = 0
		else:
			eggless_price = request.POST["eggless_price"]

		if "weight_variant" not in request.POST:
			weight_variant = None
		else:
			weight_variant = request.POST.getlist("weight_variant")

		if "weight_05_price" not in request.POST:
			weight_05_price = 0
		else:
			weight_05_price = request.POST["weight_05_price"]

		if "weight_1_price" not in request.POST:
			weight_1_price = 0
		else:
			weight_1_price = request.POST["weight_1_price"]

		if "weight_15_price" not in request.POST:
			weight_15_price = 0
		else:
			weight_15_price = request.POST["weight_15_price"]

		if "weight_2_price" not in request.POST:
			weight_2_price = 0
		else:
			weight_2_price = request.POST["weight_2_price"]

		if "box_variant" not in request.POST:
			box_variant = None
		else:
			box_variant = request.POST.getlist("box_variant")

		if "box_1_price" not in request.POST:
			box_1_price = 0
		else:
			box_1_price = request.POST["box_1_price"]

		if "box_2_price" not in request.POST:
			box_2_price = 0
		else:
			box_2_price = request.POST["box_2_price"]

		if "box_3_price" not in request.POST:
			box_3_price = 0
		else:
			box_3_price = request.POST["box_3_price"]

		if "box_4_price" not in request.POST:
			box_4_price = 0
		else:
			box_4_price = request.POST["box_4_price"]

		if "box_5_price" not in request.POST:
			box_5_price = 0
		else:
			box_5_price = request.POST["box_5_price"]

		if "box_6_price" not in request.POST:
			box_6_price = 0
		else:
			box_6_price = request.POST["box_6_price"]

		new_product = Product.objects.create(title=product_title, slug=product_title)
		new_product.baker = get_baker
		new_product.product_type = ProductType.objects.get(title=product_by_type)
		new_product.category = Category.objects.get(title=product_by_category)
		new_product.description = product_description
		new_product.veg_or_nonveg = product_veg_or_nonveg
		new_product.save()

		# EGG VARIATION 
		for item in egg_or_eggless_variant:
			if item == "Egg":
				new_egg_variant = EggVariations.objects.create(egg_variation_type=item)
				new_egg_variant.product = Product.objects.get(id=new_product.id)
				new_egg_variant.extra_price = egg_or_eggless_price
				new_egg_variant.save()
			if item == "Eggless":
				new_egg_variant = EggVariations.objects.create(egg_variation_type=item)
				new_egg_variant.product = Product.objects.get(id=new_product.id)
				new_egg_variant.extra_price = eggless_price
				new_egg_variant.save()

		# WEIGHT VARIANT SECTION
		if weight_variant == None:
			pass
		else:
			for item in weight_variant:
				if item == "0_5Kg":
					new_weight_variant = WeightVariations.objects.create(weight_variation_type="0.5 Kg")
					new_weight_variant.product = Product.objects.get(id=new_product.id)
					new_weight_variant.price = weight_05_price
					new_weight_variant.save()
				if item == "1Kg":
					new_weight_variant = WeightVariations.objects.create(weight_variation_type="1 Kg")
					new_weight_variant.product = Product.objects.get(id=new_product.id)
					new_weight_variant.price = weight_1_price
					new_weight_variant.save()
				if item == "1_5Kg":
					new_weight_variant = WeightVariations.objects.create(weight_variation_type="1.5 Kg")
					new_weight_variant.product = Product.objects.get(id=new_product.id)
					new_weight_variant.price = weight_15_price
					new_weight_variant.save()
				if item == "2Kg":
					new_weight_variant = WeightVariations.objects.create(weight_variation_type="2 Kg")
					new_weight_variant.product = Product.objects.get(id=new_product.id)
					new_weight_variant.price = weight_2_price
					new_weight_variant.save()

		#weight Variation Section
		if box_variant == None:
			pass
		else:
			for item in box_variant:
				if item == "1_Box":
					new_box_variant = BoxVariations.objects.create(box_variation_type="1 Box")
					new_box_variant.product = Product.objects.get(id=new_product.id)
					new_box_variant.price = box_1_price
					new_box_variant.save()
					print "Step1"

				if item == "2_Box":
					new_box_variant = BoxVariations.objects.create(box_variation_type="2 Box")
					new_box_variant.product = Product.objects.get(id=new_product.id)
					new_box_variant.price = box_2_price
					new_box_variant.save()
					print "Step2"

				if item == "3_Box":
					new_box_variant = BoxVariations.objects.create(box_variation_type="3 Box")
					new_box_variant.product = Product.objects.get(id=new_product.id)
					new_box_variant.price = box_3_price
					new_box_variant.save()
					print "Step3"

				if item == "4_Box":
					new_box_variant = BoxVariations.objects.create(box_variation_type="4 Box")
					new_box_variant.product = Product.objects.get(id=new_product.id)
					new_box_variant.price = box_4_price
					new_box_variant.save()
					print "Step4"

				if item == "5_Box":
					new_box_variant = BoxVariations.objects.create(box_variation_type="5 Box")
					new_box_variant.product = Product.objects.get(id=new_product.id)
					new_box_variant.price = box_5_price
					new_box_variant.save()
					print "Step5"

				if item == "6_Box":
					new_box_variant = BoxVariations.objects.create(box_variation_type="6 Box")
					new_box_variant.product = Product.objects.get(id=new_product.id)
					new_box_variant.price = box_6_price
					new_box_variant.save()
					print "Step6"

		success_url = "/superadmin/baker/baker_details/%s/" %(get_baker.slug)
		return HttpResponseRedirect(success_url)
	template = "superadmin/products/superadmin_product_add.html"
	context = {
		"site_title": "Add New Product",
		"baker": get_baker,
		"categories":categories,
		"product_types": product_types

	}
	return render(request, template, context)

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_product_update(request, slug):
	product = get_object_or_404(Product, slug=slug)
	if request.method == "POST":
		pass

	template = "superadmin/products/superadmin_product_update.html"
	
	context = {
		"site_title": "Update Product"+product.title,
		"product":product,
	}

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_orders_list(request):
	"""Displays products list for each baker"""
	template = "superadmin/order/superadmin_orders_list.html"
	context = {
		"site_title": "Orders List",

	}
	return render(request, template, context)

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_order_view(request):
	template = "superadmin/order/superadmin_order_list.html"
	context = {
		"site_title": "Orders List"
	}
	return render(request, template, context)


class OrderListJSON(BaseDatatableView):

	model = OrderHistory
	columns = ['order id',  'purchased on', 'customer','total', 'approve', 'notify_customer', 'action']
	order_columns =  ['order id', '-timestamp', 'user', 'approve', 'notify_customer']
	max_display_length = 500
	def render_column(self, row, column):
		if column == 'order id':
			return row.main_order_id
		elif column == 'purchased on':
			return row.timestamp.strftime('%d %b, %Y - %I:%M:%S')
		elif column == 'customer':
			return '%s %s' %(row.user.first_name, row.user.last_name)
		elif column == 'total':
			return '%s' % row.get_all_final_total()
		elif column == 'approve':
			if row.approve == True:
				return '<span class="badge badge-success"><i class="fa fa-check"></span>'
			elif row.approve == False:
				return '<span class="badge badge-danger"><i class="fa fa-times"></span>'
		elif column == 'notify_customer':
			if row.notify_customer == True:
				return '<span class="badge badge-success"><i class="fa fa-check"></span>'
			elif row.notify_customer == False:
				return '<span class="badge badge-danger"><i class="fa fa-times"></span>'
		elif column == 'action':
			order_detail_url = reverse('superadmin_order_details', args=(row.main_order_id,))
			return '<a href="%s" class="btn btn-sm btn-circle btn-default btn-editable"><i class="fa fa-search"></i> View</a>' %order_detail_url
		else:
			return super(OrderListJSON, self).render_column(row, column)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(OrderListJSON, self).dispatch(request, *args, **kwargs)



@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_order_details(request, main_order_id):
	get_main_order = OrderHistory.objects.get(main_order_id=main_order_id)
	shipping_details = OrderShippingDetails.objects.get(main_order=get_main_order)
	get_useraccount = UserAccount.objects.get(user=shipping_details.user)
	context = {
		"site_title": "Order Detail",
		"get_main_order": get_main_order,
		"shipping_details":shipping_details,
		"get_useraccount":get_useraccount,
	}
	template = "superadmin/order/superadmin_order_details.html"
	return render(request, template, context)

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_quick_order_status_update(request, order_id):
	get_order = Order.objects.get(order_id=order_id)
	main_order = get_order.orderhistory_set.all()
	if request.method == "POST" and request.is_ajax:
		status_update = {}
		if 'status' not in request.POST:
			status = "Pending"
			status_update['result'] = "failed"
		else:
			status = request.POST['status']
			get_order.status = status
			get_order.save()
			status_update['result'] = "success"
		return HttpResponse(JsonResponse(status_update))
	success_url = "/superadmin/order_detail/%s/" %(main_order)
	print success_url
	return HttpResponseRedirect(success_url)

@user_passes_test(lambda u:u.is_superuser, login_url='/superadmin/')
def superadmin_order_update(request, main_order_id):
	get_main_order = OrderHistory.objects.get(main_order_id=main_order_id)
	context = {
		"site_title": "Order Update",
	}
	template = "superadmin/order/superadmin_order_update.html"
	return render(request, template, context)
	



# Superadmin MCB VIEWS

