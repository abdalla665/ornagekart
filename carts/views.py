from msilib import CAB
from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

#
# this function gets the session id and return it
def _cart_id(request):
    cart = request.session.session_key #get the session key and store it
    if not cart: #if there is no session key , make one
        cart = request.session.create()
    return cart


def add_cart(request, product_id): #gets the product by id from template by urls
    product = Product.objects.get(id=product_id) #now we have this product we choose in a var called product
    try:
        cart =  Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist: # if dont exist make a new one
        cart = Cart.objects.create(cart_id= _cart_id(request)) #make the id of the cart to be the session key
    cart.save()
    #next
    try: # put the product inside the cart and call it cart_item

        cart_item = CartItem.objects.get(product=product, cart=cart) #get an object in the CartItem model
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product = product, quantity=1,cart=cart) #create an object in the CartItem model
        cart_item.save()
    return redirect('cart')




def cart(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2* total)/100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total' : grand_total
        
    }
    return render(request,'store/cart.html',context)


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
            cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
    
