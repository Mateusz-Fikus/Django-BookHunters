
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import offer
from django.contrib.auth.decorators import login_required



# Create your views here.

def all_offers(request):
    offers_all = offer.objects.all()

    return render(request, 'all_offers.html', {'offers': offers_all, 'title': 'all books!'})


def offer_info(request, id):
    offer_get = get_object_or_404(offer, pk=id)
    return render(request, 'offer_info.html', {'offer': offer_get, 'title': offer_get.title})

@login_required
def new_offer(request):
    return redirect('/')
    



def delete_offer(request, id):

    offert = offer.objects.get(id=id)
    

    #DOMYŚLNIE OFFER.ID_OWNER_USER ZWRACA EMAIL WLASCICIELA - NALEŻY DODAĆ .id
    if offert.id_owner_user.id == request.user.id:
        offert.delete()
        return redirect('my_offers')

    else:
        return redirect('all_offers')






@login_required
def my_offers(request):
    offers_all = offer.objects.filter(id_owner_user = request.user.id)
    return render(request, 'my_offers.html', {'offers': offers_all, 'title': 'Moje oferty'})

@login_required
def accept_offer(request):
    return redirect('/')

