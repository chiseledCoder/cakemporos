from django.contrib import admin
from .models import *
# Register your models here.

def enable_selected_localitys(modeladmin, request, queryset):
    queryset.update(status=True)
    enable_selected_localitys.short_description = "Enable selected localities"

def disable_selected_localitys(modeladmin, request, queryset):
    queryset.update(status=False)
    disable_selected_localitys.short_description = "Disable selected localities"


class LocalityAdmin(admin.ModelAdmin):
    list_display = [
        'locality_name',
        'pincode',
        'status',
    ]
    filters = ['status']
    search_fields = ['locality_name' ]
    actions = [enable_selected_localitys, disable_selected_localitys]

class SubLocalityAdmin(admin.ModelAdmin):
    list_display = [
        'locality',
        'sub_locality',
        'timestamp',
    ]

class OffersAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'get_image',
        'status',
    ]

admin.site.register(Locality, LocalityAdmin)
admin.site.register(Sub_Locality)
admin.site.register(About)
admin.site.register(FAQ)
admin.site.register(Offers, OffersAdmin)