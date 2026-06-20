from django.shortcuts import redirect, render
from products.models import Product


def view_cart(request):
    """Display the shopping cart."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
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

    return redirect('view_cart')