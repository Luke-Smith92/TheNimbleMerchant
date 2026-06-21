from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
]
from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')