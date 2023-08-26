from django.contrib import admin
from cart.models import CartItem, Cart
# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
    	'id',
        'cart',
        'product',
        'addon',
        
    ]

class CartAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'sub_total',
		'service_charge_value',
		'total',
		'coupon',
		'locality'
	]
		
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
