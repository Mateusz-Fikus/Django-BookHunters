from django.views.decorators.cache import cache_control

from django.contrib import messages 


from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import offer, pending
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .forms import OfferForm
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


def all_offers(request):
    offers_all = offer.objects.filter(id_buyer__isnull=True)

    return render(request, 'all_offers.html', {'offers': offers_all, 'title': 'all books!'})

def offer_info(request, id):
    offer_get = get_object_or_404(offer, pk=id)

    if request.method == "POST" and offer_get.id_buyer == None and request.user.id != offer_get.id_owner_user.id :

        owner = User.objects.get(id=offer_get.id_owner_user.id)
        pending_req = pending()
        check = pending.objects.filter(id_offer=id).filter(id_intrested=request.user.id)
        
        if not check:
            pending_req.id_offer = offer_get
            pending_req.id_intrested = User.objects.get(id=request.user.id)
            pending_req.id_owner = owner
            pending_req.message = request.POST['message']
            pending_req.save()
            return redirect('/')

        else:
            messages.info(request, 'You allready want that book!')
            
    return render(request, 'offer_info.html', {'offer': offer_get, 'title': offer_get.title})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def new_offer(request):

    form = OfferForm()

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            offer = form.save(commit=False)
            offer.id_owner_user = user
            form.save()

            #return render(request, 'offer_info.html', {'offer': offer, 'title':offer.title})
            #return render(request, 'view_profile', )
            return HttpResponseRedirect(reverse('offer_info', args=[offer.id]))

    return render(request, 'form_offer.html', {'form': form, 'title':'Add offer'})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit_offer(request, id):

    offer_ed = get_object_or_404(offer, pk=id)

    if request.user.id != offer_ed.id_owner_user.id:

        return redirect('/')

    messages.info(request, 'WARNING! Editing offer will delete all current purchase requests for that offer!')

    form = OfferForm(request.POST or None, request.FILES or None, instance=offer_ed)

    if form.is_valid():
        interested_users = pending.objects.filter(id_offer=offer_ed)
        interested_users.delete()
        form.save()
        return HttpResponseRedirect(reverse('offer_info', args=[offer_ed.id]))

    return render(request, 'form_offer.html', {'form': form, 'title': 'Edit offer'})

@login_required(login_url='login')
def delete_offer(request, id):

    offert = offer.objects.get(id=id)
    if request.user.id == offert.id_owner_user.id:

        pendings = pending.objects.filter(id_offer=offert)
        pendings.delete()
        offert.delete()

    else:
         return HttpResponseNotFound()
    
    #zwrot do tej samej strony
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def pending_requests(request, id):

    pen_offer = offer.objects.get(id=id)
 
    if pen_offer.id_owner_user.id == request.user.id and pen_offer.id_buyer is None:
        buyers = pending.objects.filter(id_offer=id)
        print(buyers)
        return render(request, 'pending.html', {'buyers': buyers, 'title': 'Pending requests', 'book_title': pen_offer.title})

    else:
        return redirect('/')

def sell(request, id_offer, id_user):

    if request.user.id == id_user:
        return redirect('/')    

    else:

        sold_offer = offer.objects.get(id=id_offer)
        pendings = pending.objects.filter(id_offer=id_offer)
        pendings.delete()
        sold_offer.id_buyer = User.objects.get(id=id_user)
        sold_offer.save()

        return HttpResponseRedirect(reverse('offer_info', args=[sold_offer.id]))

@login_required(login_url='login')
def history(request):

    wanted = pending.objects.filter(id_intrested=User.objects.get(id=request.user.id))
    bought_books = offer.objects.filter(id_buyer=User.objects.get(id=request.user.id))

    print(wanted)

    return render(request, 'history.html', {'pendings': wanted, 'bought': bought_books, 'title': 'My history'})

@login_required(login_url='login')
def cancel(request, id):
    canceled = pending.objects.get(id=id)
    if canceled.id_intrested.id == request.user.id:
        canceled.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')
