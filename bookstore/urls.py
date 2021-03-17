from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

#Z CZYSTEGO LINKA

urlpatterns = [

    path('', views.main, name='mainpage'),
    path('users/', include('users.urls')),
    path('offers/', include('offers.urls')),
    path('test', views.test)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)