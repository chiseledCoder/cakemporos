# import logging

# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from order.models import Order
# from accounts.models import UserAccount

# @receiver(post_save, sender=Order)
# def send_customer_and_baker_approval_sms(sender, instance, **kwargs):
# 	print "Helo"
# 	# if instance.approve = True:
# 	# 	print "Sending SMS"
# 	# else:
# 	# 	print "SMS not sent"

# post_save.connect(post_save, sender=Order)
