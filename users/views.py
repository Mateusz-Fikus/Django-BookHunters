from django.shortcuts import render, redirect, get_object_or_404


#FORMULARZE



#POBIERANIE OFERT OD DANEGO UŻYTKOWNIKA NA PROFIL
from offers.models import offer
#POBIERANIE ZDJECIA NA PROFIL
from users.models import UserProfilePicture


#JEŚLI NIE MA OFERT I ZDJECIA / DOES NOT EXIST
from django.core.exceptions import ObjectDoesNotExist


#DO MAILA
from ksiegarnia.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

#TOKENY WERYFIKACJI KONTA MAILEM
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
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
        picture = UserProfilePicture.objects.get(id=19)

    return render(request, 'profile.html', {'user': user_prof, 'offers': user_offers, 'profile_pic': picture, 'title': user_prof.username})



#little change


#FORMULARZ REJESTRACYJNY

def register(request):



    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        user = get_user_model()
        if password1 == password1:
            if User.objects.filter(username=username).exists():
                print('username taken')
                messages.info(request, 'username taken')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email allready exists')
            else:
                user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, phone_number = phone_number, password = password1)
                user.save()


#WYSYŁANIE MAILA Z TOKENEM AKTYWACJI KONTA

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = 'http://' + domain + link
                subject = 'witamy na pizdowce'
                message = 'Hej ' + user.username + ' Please verify your account by clicking this link\n' + activate_url
                recipient = str(email)
                send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently = False)

                messages.info(request, 'Please verify your account by confirmation email')
                return render(request, 'login.html',  {'title' : "login"})
                #return redirect('/')
        else:
            messages.info(request, 'passwords arent matching')

        
    return render(request, 'rejestracja.html',  {'title' : "Rejestracja"})

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

def logout(request):
    auth.logout(request)
    return redirect('/')

def activate(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        print(id)
        user = User.objects.get(pk=id)
        print(user)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(token)

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        
        return redirect('login.html')
    else:
        return redirect('/')





