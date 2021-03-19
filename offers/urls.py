from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('all/', views.all_offers, name='all_offers'),
    path('<id>', views.offer_info, name='offer_info'),
    path('new_offer/', views.new_offer, name='new_offer'),
    path('delete/<id>', views.delete_offer, name='delete_offer'),
    path('edit/<id>', views.edit_offer, name='edit_offer'),
    path('request_offer/<id>', views.request_offer, name='request_offer'),
    path('pending/<id>', views.pending_requests, name='pending'),
    path('sell/<id_offer>/<id_user>', views.sell, name='sell')
]
