from accounts.models import *

def get_user_account(request):
	user = request.user
	useraccount = UserAccount.objects.get(user=user)
	context ={
		"useraccount": useraccount,
	}

# def is_user_active(request):
# 	if request.user is not None:
# 		user = request.user
# 		if user.is_active:
# 			context = {
# 				"user_not_active" : "user_not_active"
# 			}
# 		else:
# 			context ={
# 				"user_active" : "user_active"
# 			}
# 	else:
# 		pass
	