from decimal import Decimal

from django.shortcuts import render, redirect

from .models import Order, OrderLineItem
from products.models import Product


def checkout(request):

    if request.method == "POST":

        order = Order.objects.create(
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone_number=request.POST.get("phone_number"),
            address=request.POST.get("address"),
            town_or_city=request.POST.get("town_or_city"),
            postcode=request.POST.get("postcode"),
        )

        cart = request.session.get("cart", {})

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

    return render(request, "checkout/checkout.html")