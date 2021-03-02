from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()



def main(request):
    uname = request.user.username
    return render(request, 'main.html', {'username': uname})



