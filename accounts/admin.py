from django.contrib import admin
from accounts.models import *
# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'phone',
		'coupons_list',	]

class UserAddressesAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'user_addresses'
	]

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserAddresses, UserAddressesAdmin)