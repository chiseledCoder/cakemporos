from django.contrib import admin
from .models import Baker
# Register your models here.

class BakerAdmin(admin.ModelAdmin):
	list_display = [
        'owner',
        'shop_name',
        'veg_or_nonveg',
        'serving_locality_list'
    ]
	list_filter = ('veg_or_nonveg','owner')

admin.site.register(Baker, BakerAdmin)