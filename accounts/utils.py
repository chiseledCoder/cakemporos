import string
import random

from .models import UserAccount
def reward_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		reward = UserAccount.objects.get(reward_id=the_id)
		id_generator()
	except UserAccount.DoesNotExist:
		return the_id