from django.conf.urls import url, include
from django.conf import settings
from mycakebox_baker import views
                            

urlpatterns = [
	url(r'^mycakebox/book/$', views.mycakebox_baker_book, name='mycakebox_baker_book'),
    url(r'^mycakebox/get_distance/$', views.get_distance, name='get_distance'),
	
]



#for Class based view follow below syntax
#url(r'^mydashboard/baker/create/$', ViewName.as_view(), name='view_name'),
#for function based view follow below syntax
#url(r'^mydashboard/$', 'model.views.view_name', name='view_name'),