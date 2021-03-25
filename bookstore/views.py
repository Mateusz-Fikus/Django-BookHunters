from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from offers import filters
from offers.models import offer
from offers.filters import OfferFilter 
User = get_user_model()



def main(request):

    uname = request.user.username
    offers = offer.objects.filter(id_buyer=None)
    filter = OfferFilter(request.GET, queryset=offers)
    offers = filter.qs



    return render(request, 'dashboard.html', {'username': uname, 'offers': offers, 'filter': filter})


