from django.views.decorators.cache import cache_control

from django.contrib import messages 


from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import offer, pending
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .forms import OfferForm

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


def all_offers(request):
    offers_all = offer.objects.filter(id_buyer__isnull=True)

    return render(request, 'all_offers.html', {'offers': offers_all, 'title': 'all books!'})

def offer_info(request, id):
    offer_get = get_object_or_404(offer, pk=id)
    print(offer_get.id)

    print(request.user.is_authenticated)



    if request.method == "POST" and offer_get.id_buyer == None:

        owner = User.objects.get(id=offer_get.id_owner_user.id)
        pending_req = pending()
        check = pending.objects.filter(id_offer=id).filter(id_intrested=request.user.id)
        

        print(check)

        if not check:
            pending_req.id_offer = offer_get
            pending_req.id_intrested = User.objects.get(id=request.user.id)
            pending_req.id_owner = owner
            pending_req.message = request.POST['message']
            pending_req.save()
            return redirect('/')

        else:
            messages.info(request, 'Yo allready want it')
            


    
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
            return redirect('/')

    return render(request, 'form_offer.html', {'form': form, 'title':'Add offer'})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit_offer(request, id):

    offer_ed = get_object_or_404(offer, pk=id)

    if request.user.id != offer_ed.id_owner_user.id:

        return redirect('/')


    form = OfferForm(request.POST or None, request.FILES or None, instance=offer_ed)

    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'form_offer.html', {'form': form, 'title': 'Edit offer'})


@login_required(login_url='login')
def delete_offer(request, id):

    offert = offer.objects.get(id=id)
    
    #DOMYŚLNIE OFFER.ID_OWNER_USER ZWRACA EMAIL WLASCICIELA (__str__ z modelu - email) - NALEŻY DODAĆ .id
    if offert.id_owner_user.id == request.user.id:
        offert.delete()
        return redirect('my_offers')

    else:
         return HttpResponseNotFound()


@login_required(login_url='login')
def request_offer(request, id):
    selected_offer = offer.objects.get(id=id)

    if selected_offer.id_owner_user.id == request.user.id:
        redirect('/')
    

    selected_offer.id_buyer = User.objects.get(id=request.user.id)
    selected_offer.save()
    return redirect('/')

@login_required(login_url='login')
def pending_requests(request, id):

    pen_offer = offer.objects.get(id=id)
 
    if pen_offer.id_owner_user.id == request.user.id and pen_offer.id_buyer is None:
        buyers = pending.objects.filter(id_offer=id)
        print(buyers)
        return render(request, 'pending.html', {'buyers': buyers, 'title': 'Pending requests'})

    else:
        return redirect('/')

def sell(request, id_offer, id_user):

    #pendings = pending.objects.get()

    if request.user.id == id_user:
        return redirect('/')    

    else:

        sold_offer = offer.objects.get(id=id_offer)
        pendings = pending.objects.filter(id_offer=id_offer)
        pendings.delete()
        sold_offer.id_buyer = User.objects.get(id=id_user)
        sold_offer.save()

        return redirect('/')





