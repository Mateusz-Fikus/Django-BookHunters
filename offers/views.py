
from django.shortcuts import render, redirect, get_object_or_404
from .models import offer

# Create your views here.


def all_offers(request):
    offers_all = offer.objects.all()
    print(offers_all)
    return render(request, 'all_offers.html', {'offers': offers_all})


def offer_info(request, id):
    offer_get = get_object_or_404(offer, pk=id)
    return render(request, 'offer_info.html', {'offer': offer_get})

def accept_offer(request):
    return redirect('/')