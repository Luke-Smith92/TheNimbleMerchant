from django.shortcuts import render


def checkout(request):
    """Display checkout page."""
    return render(request, 'checkout/checkout.html')