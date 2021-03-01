from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import offer

# Create your views here.


def all_offers(request):
    return redirect('/')