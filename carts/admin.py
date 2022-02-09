# Django modules
from django.contrib import admin

# Django locals
from carts.models import Cart, CartItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)