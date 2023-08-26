from django.conf.urls import include, url
from django.conf.urls.static import static #for developement server
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.contrib.staticfiles import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'cakemporos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('bakers.urls')),
    url(r'^', include('catalog.urls')),
    url(r'^', include('cart.urls')),
    url(r'^', include('core.urls')),
    url(r'^', include('order.urls')),
    url(r'^', include('sales.urls')),
    url(r'^', include('mybaker.urls')),
    url(r'^', include('mycakebox_baker.urls')),
    url(r'^', include('superadmin.urls')),
    url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    url(r'^media/(?P<path>.*)$', views.static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}),
]
#for development server
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
