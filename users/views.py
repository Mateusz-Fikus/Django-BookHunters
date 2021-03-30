import os
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404



#FORMULARZE
from .forms import RegistrationForm
from django.contrib.auth.forms import SetPasswordForm

#POBIERANIE OFERT OD DANEGO UŻYTKOWNIKA NA PROFIL
from offers.models import offer
#POBIERANIE ZDJECIA NA PROFIL
from users.models import UserProfilePicture


#JEŚLI NIE MA OFERT I ZDJECIA / DOES NOT EXIST
from django.core.exceptions import ObjectDoesNotExist


from users.utils import email

#TOKENY WERYFIKACJI KONTA MAILEM
from django.utils.encoding import force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from users.utils import token_generator
from django.urls import reverse


from django.contrib import auth

#DO PRZESYŁANIA INFO O BLEDNYCH DANYCH
from django.contrib import messages 

#DO DODAWANIA UZYTKOWNIKA DO BAZY DANYCH I LOGINU PRZY CUSTOMOWYM UŻYTKOWNIKU
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()



#WYSWIETLANIE PROFILU Z OFERTAMI I ZDJECIEM PROFILOWYM

def view_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    
#GET - NAZWA_MODELU.DOESNOTEXIST
    user_offers = offer.objects.filter(id_owner_user=user_prof.id).filter(id_buyer=None)
    user_sold_offers = offer.objects.filter(id_owner_user=user_prof.id).exclude(id_buyer=None)

    if not user_sold_offers:
        user_sold_offers = None

    if not user_offers:
        user_offers = None
        
    try:
        picture = UserProfilePicture.objects.get(user=user_prof.id)
#W RAZIE BRAKU ZDJECIA PROFILOWEGO WYBIERANE JEST DOMYSLNE ZDJECIE
    except UserProfilePicture.DoesNotExist:
        picture = None

#ZMIANA ZDJECIA PROFILWOEGO
    if request.method == 'POST':
        if request.user.id == user_prof.id:
            if len(request.FILES) != 0:
                image = request.FILES['image']
                try:
                    image = request.FILES['image']
                    picture = UserProfilePicture.objects.get(user=request.user.id)
                    picture.photo = image
                    picture.save()
                except:
                    picutre = UserProfilePicture()
                    picture.user = User.objects.get(id=request.user.id)
                    picture.photo = image
                    picture.save()                    
            else:
                print("No files uploaded")

    return render(request, 'profile.html', {'user': user_prof, 'offers': user_offers, 'profile_pic': picture, 'title': user_prof.username
    , 'sold_offers': user_sold_offers,   
    })

def register(request):

    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = RegistrationForm()

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.get(username=form.data['username'])

                #EMAIL AKTYWACYJNY
                email("REG", **{"user": user, "domain":get_current_site(request).domain})
                return redirect('login')

        return render(request, 'register.html',  {'title' : "Register", 'form': form})

def forgot_password(request):

    if request.method == 'POST':
        user_email = request.POST['email']

        try:
           user = User.objects.get(email=user_email)
        except(User.DoesNotExist):
            messages.info(request, 'Invalid email')
        
        if user_email is not None:
            
            email("RES", **{"user": user, "domain":get_current_site(request).domain})

            messages.info(request, 'Password reset email has been sent!')

            return redirect('login')

    return render(request, 'forgot_password.html', {'title':'Password reset'})


def reset_pasword(request, uidb64, token):
    form = SetPasswordForm(User)
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return redirect('/')
    
    if user is not None and token_generator.check_token(user, token):

        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')

        return render(request, 'reset_password.html', {'title':'reset', 'form':form})
    else:
        redirect('/')

    print(token_generator.check_token(user, token))
    print('dzialas')
    return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        User = auth.authenticate(username=email, password=password)

        if User is not None:
            auth.login(request, User)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')

    return render(request, 'login.html', {'title' : "Login"})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def logout(request):
    if request.method == 'POST':

        auth.logout(request)
        return redirect('login')
    return render(request, 'logout.html')

def activate(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        print(user)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/')

    return redirect('/')

