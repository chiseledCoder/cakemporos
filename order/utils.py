import string
import random


from .models import Order, OrderHistory


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		order = Order.objects.get(order_id=the_id)
		id_generator()
	except Order.DoesNotExist:
		return the_id

def main_id_generator(size=5, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		order = OrderHistory.objects.get(main_order_id=the_id)
		main_id_generator()
	except OrderHistory.DoesNotExist:
		return the_id