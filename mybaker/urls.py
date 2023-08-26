from django.conf.urls import url, include
from django.conf import settings
from mybaker import views
                            

urlpatterns = [
	url(r'^mybaker/logout/$', views.mybaker_logout_view, name='mybaker_logout'),
    url(r'^mybaker/$', views.mybaker_login_view, name='mybaker_login'),
	url(r'^mybaker/dashboard/$', views.mybaker_dashboard, name='mybaker_dashboard'),
	url(r'^mybaker/orders/$', views.mybaker_orders_list, name='mybaker_orders_list'),
	url(r'^mybaker/orders/order_details/(?P<order_id>\w+)/$', views.mybaker_order_detail, name='mybaker_order_detail'),
	url(r'^mybaker/orders/order_details/order_status_update/(?P<order_id>\w+)/$', views.mybaker_order_status_update, name='mybaker_order_status_update'),
	url(r'^mybaker/orders/payment_clearance/$', views.mybaker_payment_clearance, name='mybaker_payment_clearance'),
	url(r'^mybaker/products/$', views.mybaker_products_list, name='mybaker_products_list'),   
	#url(r'^mybaker/products/add_product/$', views.mybaker_add_new_product, name='mybaker_add_new_product'),
	url(r'^mybaker/products/update/(?P<slug>[\w-]+)/$', views.mybaker_update_product, name='mybaker_update_product'),
	
]



#for Class based view follow below syntax
#url(r'^mydashboard/baker/create/$', ViewName.as_view(), name='view_name'),
#for function based view follow below syntax
#url(r'^mydashboard/$', 'model.views.view_name', name='view_name'),