from django.conf.urls import url, include
from django.conf import settings
from superadmin import views
from superadmin.views import *  

urlpatterns = [
	url(r'^superadmin/logout/$', views.superadmin_logout_view, name='superadmin_logout'),
    url(r'^superadmin/$', views.superadmin_login_view, name='superadmin_login'),
	url(r'^superadmin/dashboard/$', views.superadmin_dashboard, name='superadmin_dashboard'),
	url(r'^superadmin/baker/bakers_list/$', views.superadmin_bakers_list, name='superadmin_bakers_list'),
	url(r'^superadmin/baker/bakers_json', BakersListJSON.as_view(), name='bakers_list_json'),
	url(r'^superadmin/baker/baker_details/(?P<slug>[\w-]+)/$', views.superadmin_baker_details, name='superadmin_baker_details'),
	url(r'^superadmin/baker/baker_details/(?P<slug>[\w-]+)/products_json/$', ProductsListByBakerJson.as_view(), name='products_by_baker_json'),
	url(r'^superadmin/baker/baker_details/(?P<slug>[\w-]+)/orders_json/$', OrdersListByBakerJson.as_view(), name='orders_by_baker_json'),
	# url(r'^superadmin/products/$', views.superadmin_product_list, name='superadmin_product_list'),   
	url(r'^superadmin/baker/baker_details/(?P<slug>[\w-]+)/add_product/$', views.superadmin_add_new_product, name='superadmin_add_new_product'),
	url(r'^superadmin/orders_list/$', views.superadmin_orders_list, name='superadmin_orders_list'),
	url(r'^superadmin/order_detail/(?P<main_order_id>\w+)/$', views.superadmin_order_details, name='superadmin_order_details'),
	url(r'^superadmin/orders_list/orders_json/', OrderListJSON.as_view(), name='orders_list_json'),
	url(r'^superadmin/order/order_status_update/(?P<order_id>\w+)/$', views.superadmin_quick_order_status_update, name='superadmin_quick_order_status_update'),
	url(r'^superadmin/order/order_update/(?P<main_order_id>\w+)/$', views.superadmin_order_update, name='superadmin_order_update')
	# url(r'^superadmin/order_status_update/(?P<order_id>\w+)$', views.mybaker_order_status_update, name='mybaker_order_status_update'),
]



#for Class based view follow below syntax
#url(r'^mydashboard/baker/create/$', ViewName.as_view(), name='view_name'),
#for function based view follow below syntax
#url(r'^mydashboard/$', 'model.views.view_name', name='view_name'),