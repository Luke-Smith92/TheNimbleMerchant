from decimal import Decimal
from django.shortcuts import redirect, render
from products.models import Product

def view_cart(request):
    """Display the shopping cart."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if total >= Decimal("50.00"):
        delivery = Decimal("0.00")
    else:
        delivery = Decimal("3.99")

    grand_total = total + delivery

    context = {
        'cart_items': cart_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    """Add a product to the shopping cart."""
    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    request.session['cart'] = cart

    return redirect('product_detail', product_id=product_id)

def update_cart(request, product_id):
    """Update product quantity in cart."""

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)

    request.session['cart'] = cart
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    """Remove item from cart."""

    cart = request.session.get('cart', {})

    cart.pop(str(product_id), None)

    request.session['cart'] = cart

    return redirect('view_cart')