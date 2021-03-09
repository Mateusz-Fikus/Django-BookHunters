from django import forms
from django.forms import ModelForm
from .models import offer

from django.contrib.auth.forms import AuthenticationForm








class OfferForm(ModelForm):
    class Meta:
        model = offer
        fields = ['title', 'desc', 'price', 'front_picture', 'back_picture', 'genre']
  


