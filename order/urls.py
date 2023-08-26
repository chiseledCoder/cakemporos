from django.conf.urls import include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^order_confirm$', views.order_confirm, name='order_confirm'),
    url(r'^order_email$', TemplateView.as_view(template_name='orders/order_email.html')),
    url(r'^calculate_delivery_charge/(?P<id>\d+)$', views.calculate_delivery_charge, name='calculate_delivery_charge'),
]