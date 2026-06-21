from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from .forms import CustomUserCreationForm


def register(request):
    """Register a new user and send a welcome email."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            send_mail(
                'Welcome to The Nimble Merchant',
                f'Hi {user.username}, thank you for registering with The Nimble Merchant.',
                'thenimblemerchant@example.com',
                [user.email],
                fail_silently=False,
            )

            login(request, user)
            messages.success(request, 'Registration successful. Welcome to The Nimble Merchant!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'profiles/register.html', {'form': form})


@login_required
def profile(request):
    """Display user profile page with order history."""
    orders = Order.objects.filter(user_profile=request.user).order_by('-date')

    context = {
        'orders': orders,
    }

    return render(request, 'profiles/profile.html', context)