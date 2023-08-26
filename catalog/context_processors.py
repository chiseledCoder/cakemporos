from catalog.models import *

def get_product_category(request):
	cake_category = Category.objects.filter(title="Cake")
	cupcake_category = Category.objects.filter(title="Cupcake")
	cake_products = Product.objects.filter(category=cake_category)
	cupcake_products = Product.objects.filter(category=cupcake_category)
	return {
		"cake_products": cake_products,
		"cupcake_products": cupcake_products,
	}