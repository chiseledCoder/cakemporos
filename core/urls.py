from django.conf.urls import include, url
from . import views


urlpatterns = [
	url(r'^$', views.Index, name='userindex'),
	url(r'^about/$', views.About, name='about'),
	url(r'^terms-and-conditions/$', views.Terms, name='tnc'),
	url(r'^privacy/$', views.Privacy, name='privacy'),
	url(r'^contact/$', views.Contact, name='contact'),
	url(r'^offers/$', views.offers_page, name='offers_page'),
	url(r'^corporate/$', views.Corporate, name='corporate'),
	url(r'^delivery/$', views.Delivery, name='delivery'),
	url(r'^cake-of-the-day/$', views.Cake_Of_The_Day, name='cakeoftheday'),
	url(r'^faq/$', views.F_A_Q, name='faq'),
	url(r'^reward/$', views.RewardPage, name='reward'),
]