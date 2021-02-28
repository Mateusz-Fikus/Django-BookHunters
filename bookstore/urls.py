from django.urls import path, include
from . import views



#Z CZYSTEGO LINKA

urlpatterns = [
    path('', views.main, name='mainpage'),


]
