from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^cart/remove/(?P<id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/add_to_cart/(?P<slug>[\w-]+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/update/(?P<id>\d+)/$', views.update_cart, name='update_cart'),
    url(r'^cart/$', views.view_cart, name='cart'),
    url(r'^quick_cart/add/(?P<slug>[\w-]+)/$', views.quick_add_to_cart, name='quick_add_to_cart'),
    url(r'^quick_cart/update/(?P<id>\d+)/$', views.quick_update_cart, name='quick_update_cart'),
    url(r'^quick_cart/remove/(?P<id>\d+)/$', views.quick_remove_from_cart, name='quick_remove_from_cart'),
    url(r'^quick_addon/add/$', views.quick_addon, name='quick_addon'),
    url(r'^quick_giftitem_addtocart/add/(?P<id>\d+)$', views.quick_giftitem_addtocart, name='quick_giftitem_addtocart'),
]