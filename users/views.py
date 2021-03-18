from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control






from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import SetPasswordForm


#FORMULARZE
from .forms import RegistrationForm

#POBIERANIE OFERT OD DANEGO UŻYTKOWNIKA NA PROFIL
from offers.models import offer
#POBIERANIE ZDJECIA NA PROFIL
from users.models import UserProfilePicture


#JEŚLI NIE MA OFERT I ZDJECIA / DOES NOT EXIST
from django.core.exceptions import ObjectDoesNotExist

#DO MAILA
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

#TOKENY WERYFIKACJI KONTA MAILEM
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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

    print(request.user.is_authenticated)

    user_prof = get_object_or_404(User, username=username)
    
#KAŻDY BŁĄD MUSI MIEĆ ODDZIELNY TRY - W INNYM WYPADKU REFERENCE ERROR

#GET - NAZWA_MODELU.DOESNOTEXIST
    
    user_offers = offer.objects.filter(id_owner_user=user_prof.id)

    if not user_offers:
        user_offers = 0
        print('nie ma ofert')
    

    try:
        picture = UserProfilePicture.objects.get(user=user_prof.id)
#W RAZIE BRAKU ZDJECIA PROFILOWEGO WYBIERANE JEST DOMYSLNE ZDJECIE
    except UserProfilePicture.DoesNotExist:
        picture = None


    return render(request, 'profile.html', {'user': user_prof, 'offers': user_offers, 'profile_pic': picture, 'title': user_prof.username})



#little change


#FORMULARZ REJESTRACYJNY

def register(request):



    if request.user.is_authenticated:
        return redirect('/')
    else:

        form = RegistrationForm()

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
            # print(form.data['id'])

                user = User.objects.get(username=form.data['username'])
            #EMAIL AKTYWACYJNY
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = 'http://' + domain + link
                subject = 'witamy na pizdowce'
                message = 'Hej ' + user.username + ' Please verify your account by clicking this link\n' + activate_url
                recipient = str(user.email)
                send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently = False)

                messages.info(request, 'Please verify your account by confirmation email')
                return redirect('login')
                #return redirect('/')


        return render(request, 'register.html',  {'title' : "Register", 'form': form})

def forgot_password(request):

    if request.method == 'POST':
        user_email = request.POST['email']

        try:
           user = User.objects.get(email=user_email)
        except(User.DoesNotExist):
            messages.info(request, 'Invalid email')
        
        if user_email is not None:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('reset_password', kwargs={
                'uidb64': uidb64, 'token': token_generator.make_token(user)
            })

            reset_url = domain + link
            subject = 'Bookstore password reset'
            message = 'Hey ' + user.first_name + ', here is your password reset email. If you dont know why you got this message, do not click the following link!\n' + reset_url
            recipient = str(user_email)
            send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
            
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
            return redirect('login')
        
    else:
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
        
        return redirect('login.html')
    else:
        return redirect('/')





