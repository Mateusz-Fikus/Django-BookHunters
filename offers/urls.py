from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('all/', views.all_offers, name='all_offers'),
    path('<id>', views.offer_info, name='offer_info'),
    path('new_offer/', views.new_offer, name='new_offer'),
    path('my_offers/', views.my_offers, name='my_offers'),
    path('delete/<id>', views.delete_offer, name='delete_offer'),
    path('edit/<id>', views.edit_offer, name='edit_offer'),
    path('accept_offer/<id>', views.accept_offer, name='accept_offer')
]
