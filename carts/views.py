from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product,Variation
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _card_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()

    return cart

def add_cart(request,product_id):
    # color = request.GET['color']
    product = Product.objects.get(id=product_id)
    variation_product = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product,vatiation_category__iexact=key,variation_value__iexact=value)
                variation_product.append(variation)

            except Exception as e:
                pass

                
    # get the cart using session_id present in the session 
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _card_id(request),
        )
    cart.save()

    is_cart_item_exits = CartItem.objects.filter(product=product_id,cart=cart).exists()
    if is_cart_item_exits :
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        # existing variation --> database
        # cart or item 
        existing_variation_list = []
        id = []
        for items in cart_item:
            existing_variation = items.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(items.id)
        print(existing_variation_list)
        # current variation ---> product_variation
        if variation_product in existing_variation_list:
            index = existing_variation_list.index(variation_product)
            item_id = id[index]

            item = CartItem.objects.get(product=product_id,id = item_id)
            item.quantity +=1
            item.save()

            # increase cart item quantity
        else:
            item = CartItem.objects.create(product=product, quantity=1,cart=cart)

            if len(variation_product)> 0 :
                item.variations.clear()
                item.variations.add(*variation_product)

            item.save()

    else:
        cart_item = CartItem.objects.create(product=product, quantity=1,cart=cart)

        if len(variation_product)> 0 :
            cart_item.variations.clear()
            cart_item.variations.add(*variation_product)

        cart_item.save()

    return redirect('cart')
    
        


def cart(request,total=0,quantity=0,cart_item=None):
    print("INside Cart")
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (18 * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass

        pass
    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }
    print(context)

    return render(request, 'store/cart.html',context)


def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _card_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product,id=cart_item_id)
    try:
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except :
        pass
    return redirect('cart')

def remove_all_cart_items(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _card_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product,id=cart_item_id)

    cart_item.delete()
    return redirect('cart')




