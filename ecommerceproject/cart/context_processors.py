# cart/context_processors.py

from .models import Cart, CartItem
from .views import _cart_id

def counter(request, cart_item=None):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:  # Fixed the loop variable name
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return {'item_count': item_count}  # Fixed the return statement
