from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()



def main(request):
    uname = request.user.username
    print(get_current_site(request).domain)
    return render(request, 'dashboard.html', {'username': uname})


def test(request):
    return render(request, 'my_purchases.html')

