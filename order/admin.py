from django.contrib import admin
from order.models import *
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
	list_display = (
		'order_id',
		'baker',
		'cart',
		'cartitem',
		'sub_total',
		'discount_total',
		'final_total',
		'approve',
		'notify_baker',
		'notes'
		)
	list_filter = ['baker']

class OrderShippingDetailsAdmin(admin.ModelAdmin):
	list_display = (
		'user',
		'main_order',
		'shipping_address'
		)
		
class OrderHistoryAdmin(admin.ModelAdmin):
	"""docstring for OrderHistory"""
	list_display = (
		'main_order_id',
		'orders_list',
		'user',
		'approve',
		'notify_customer',
		'notes',
		'get_all_final_total',
		)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderShippingDetails, OrderShippingDetailsAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)