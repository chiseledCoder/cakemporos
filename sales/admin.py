from django.contrib import admin
from sales.models import *
# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'coupon_title',
        'coupon_code',
        'active',
        'bakers',
        'categories',
        'products'
    ]

admin.site.register(Coupon,CouponAdmin)