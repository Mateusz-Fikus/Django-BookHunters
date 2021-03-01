from django import forms
from django.forms import ModelForm
from .models import offer

from django.contrib.auth.forms import AuthenticationForm

class EditOffer(ModelForm):
    class Meta:
        model = offer
        fields = ['title', 'desc', 'location', 'front_picture', 'back_picture']


