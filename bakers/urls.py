from django.conf.urls import include, url
from . import views


urlpatterns = [

    url(r'^s/$', views.locality_search, name='localitysearch'),
    ]