from django.contrib import admin
from .models import GiftSeller
# Register your models here.

class GiftSellerAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'featured',
		'status'
	]
admin.site.register(GiftSeller)