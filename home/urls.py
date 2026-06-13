from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]
from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')