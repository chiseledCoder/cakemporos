from django.conf.urls import include, url
from . import views


urlpatterns = [
		url(r'^user/login$', views.user_login, name='user_login'),
		url(r'^user/logout$', views.user_logout, name='user_logout'),
		url(r'^user/signup$', views.user_signup, name='user_signup'),
		url(r'^user/new-registration-otp-verify$', views.user_otp_verification, name='user_otp_verification'),
		url(r'^user/forgotpass-send-otp$', views.forgotpass_send_otp, name='forgotpass_send_otp'),
		url(r'^user/forgotpass-verify-otp$', views.forgotpass_verify_otp, name='forgotpass_verify_otp'),
		url(r'^user/reset-password$', views.user_reset_password, name='user_reset_password'),
		url(r'^user/order_history$', views.user_order_history, name="user_order_history"),
		url(r'^user/new_address$', views.user_new_address, name="user_new_address")
		
	]