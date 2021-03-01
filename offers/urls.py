from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('all/', views.all_offers, name='all_offers'),
    path('<id>', views.offer_info, name='offer_info'),
]
