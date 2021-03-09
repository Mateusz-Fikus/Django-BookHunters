from django.urls import path
from . import views

#display profile pictures during dev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/<username>', views.view_profile, name='view_profile'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>', views.reset_pasword, name='reset_password')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)