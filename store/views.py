# Django modules
from django.shortcuts import render, get_object_or_404

# Django locals
from store.models import Product
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category

# Create your views here.


def store(request,category_slug=None):

	# Define categories and products are None
	categories = None
	products   = None

	# What if categories slug are NOT None or exist
	# Return the slugs if they are exist, or
	# return 404 error if they are not exist
	if category_slug != None:
		categories = get_object_or_404(Category, slug=category_slug)
		products   = Product.objects.filter(category=categories, is_available=True)
		# Product count
		product_count = products.count()
	else:
		# Get all the available products
		products = Product.objects.all().filter(is_available=True)
		# Counting the products
		product_count = products.count()
	
	
	
	

	# Put the available products into context dictionary
	context = {
		'products':products, # <-- 'products'  as variable
		'product_count':product_count,
		'categories': categories,
		
	}	

	return render(request, 'store/store.html', context)

def product_detail(request,category_slug,product_slug):
	# Get the slug from Category model and slug from the Product model
	try: 
		single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
		products = Product.objects.all().filter(is_available=True)
		
	except Exception as e: 
		raise e

	# Put the available products into context dictionary
	context = {
		'single_product':single_product, # <-- 'single_product'  as variable
		'products': products,
		'in_cart': in_cart,
	}
	return render(request, 'store/product_detail.html', context)





