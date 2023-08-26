from django.contrib import admin
from catalog.models import *
# Register your models here.


def enable_selected(modeladmin, request, queryset):
    queryset.update(status=True)
    enable_selected.short_description = "Enable selected"

def disable_selected(modeladmin, request, queryset):
    queryset.update(status=False)
    disable_selected_localities.short_description = "Disable selected"

class ProductAdmin(admin.ModelAdmin):
	list_filter = [
	'baker', 'product_type', 'category', 'status']
	list_display = [
        'title',
        'baker',
        'product_type',
        'category',
        'status',
        'get_image',
    ]

class PhotoCakeCustomizationAdmin(admin.ModelAdmin):
	list_display = [
		'baker',
		'weight',
		'price'
	]
	list_filter =[
		'baker'
	]

class EggVariationsAdmin(admin.ModelAdmin):
	list_display = [
		'egg_variation_type',
		'product',
		'extra_price'
	]
class WeightVariationsAdmin(admin.ModelAdmin):
	list_display = [
		'weight_variation_type',
		'product',
		'price'
	]

class BoxVariationsAdmin(admin.ModelAdmin):
	list_display = [
		'box_variation_type',
		'product',
		'price'
	]

class AddonAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'price',
		'status',
		'get_image',
	]
	actions = [enable_selected, disable_selected]

class GiftItemAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'price',
		'status',
		'get_image',
	]
		
admin.site.register(ProductType)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Addon, AddonAdmin)
admin.site.register(GiftItem, GiftItemAdmin)
admin.site.register(PhotoCakeCustomization, PhotoCakeCustomizationAdmin)
admin.site.register(CakeCustomization)
admin.site.register(EggVariations, EggVariationsAdmin)
admin.site.register(WeightVariations, WeightVariationsAdmin)
admin.site.register(BoxVariations, BoxVariationsAdmin)
admin.site.register(CakeOfTheDay)