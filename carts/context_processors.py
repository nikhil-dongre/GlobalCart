from .models import Cart,CartItem
from .views import _card_id
def counter(request):
    if 'admin' in request.path:
        return {}
    else:
        cart_count = 0
        try:
            cart = Cart.objects.get(cart_id =_card_id(request))
            cart_item = CartItem.objects.filter(cart=cart)

            for cart_item in cart_item:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
    

