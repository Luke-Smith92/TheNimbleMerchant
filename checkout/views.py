import stripe
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect

from .models import Order, OrderLineItem
from products.models import Product


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("view_cart")

    if request.method == "POST":

        order = Order.objects.create(
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone_number=request.POST.get("phone_number"),
            address=request.POST.get("address"),
            town_or_city=request.POST.get("town_or_city"),
            postcode=request.POST.get("postcode"),
        )

        total = Decimal("0.00")

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)

            OrderLineItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )

            total += product.price * quantity

        order.order_total = total
        order.save()

        request.session["cart"] = {}

        return render(
            request,
            "checkout/checkout_success.html",
            {"order": order},
        )

    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * quantity

    stripe_total = int(total * 100)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
        "total": total,
    }

    return render(request, "checkout/checkout.html", context)