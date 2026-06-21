from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')
def contact(request):
    """Display contact page."""
    return render(request, 'home/contact.html')