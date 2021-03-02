
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import offer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .forms import OfferForm

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def all_offers(request):
    offers_all = offer.objects.all()

    return render(request, 'all_offers.html', {'offers': offers_all, 'title': 'all books!'})

def offer_info(request, id):
    offer_get = get_object_or_404(offer, pk=id)
    return render(request, 'offer_info.html', {'offer': offer_get, 'title': offer_get.title})

@login_required
def new_offer(request):

    form = OfferForm()

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            offer = form.save(commit=False)
            offer.id_owner_user = user
            form.save()
            return redirect('all_offers')

    print('tutaj')
    return render(request, 'form_offer.html', {'form': form, 'title':'Add offer'})
    


def edit_offer(request, id):

    offer_ed = get_object_or_404(offer, pk=id)

    form = OfferForm(request.POST or None, request.FILES or None, instance=offer_ed)

    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'form_offer.html', {'form': form, 'title': 'Edit offer'})


def delete_offer(request, id):

    offert = offer.objects.get(id=id)
    
    #DOMYŚLNIE OFFER.ID_OWNER_USER ZWRACA EMAIL WLASCICIELA - NALEŻY DODAĆ .id
    if offert.id_owner_user.id == request.user.id:
        offert.delete()
        return redirect('my_offers')

    else:
         return HttpResponseNotFound()


@login_required
def my_offers(request):
    offers_all = offer.objects.filter(id_owner_user = request.user.id)
    return render(request, 'my_offers.html', {'offers': offers_all, 'title': 'Moje oferty'})

@login_required
def accept_offer(request):

    return redirect('/')





