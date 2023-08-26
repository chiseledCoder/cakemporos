from cart.models import *

def get_cart_items_total(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total = ((float(item.weight_price) + float(item.egg_or_eggless_price) + float(item.photo_cake_cost) + float(item.cupcake_qty_price))* item.quantity) + (float(item.addon_price) * item.addon_qty) + (float(item.giftitem_price) * item.giftitem_qty)
			item.cart_item_total = line_total
			item.save()
			new_total += line_total
		cart.sub_total = new_total
		cart.coupon = None
		cart.save()
		get_total_items = CartItem.objects.filter(cart=cart).count()
		get_cart_total = cart.sub_total
	except:
		the_id = None
		cart = None
		get_total_items = 0
		get_cart_total = 0
	return {
        "get_total_items":get_total_items,
        "get_cart_total":get_cart_total,
        "cart":cart,
    }