from django.contrib import admin
from users.models import User, UserProfilePicture
from offers.models import offer

admin.site.register(User)
admin.site.register(offer)
admin.site.register(UserProfilePicture)