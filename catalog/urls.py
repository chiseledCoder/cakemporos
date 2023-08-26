from django.conf.urls import include, url
from . import views
# (?P<slug>[\w-]+)
#(?P<id>[0-9]+)
urlpatterns = [
    url(r'^products/(?P<slug>[\w-]+)/$', views.product_detail, name='product_detail'),
    url(r'^product/(?P<id>\d+)/$', views.product_like, name='product_like'),
    ]