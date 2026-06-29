import stripe
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
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
            user_profile=request.user if request.user.is_authenticated else None,
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

        send_mail(
            "Order Confirmation - The Nimble Merchant",
            f"""
Thank you for your order, {order.full_name}.

Order Number: {order.id}

Order Total: £{order.order_total}

Your order is now being processed and will be dispatched within 1-2 working days.

Thank you for shopping with The Nimble Merchant.
""",
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=True,
        )

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