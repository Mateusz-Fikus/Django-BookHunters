from django.contrib import admin
from users.models import User, UserProfilePicture
from offers.models import offer, pending

"""
admin.site.register(User)
admin.site.register(offer)
admin.site.register(UserProfilePicture)
admin.site.register(pending)
"""


@admin.register(User)
class UserAdminSite(admin.ModelAdmin):
    list_display = ["email", "username"]

@admin.register(offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["id_owner_user", "title", "id_buyer"]


@admin.register(UserProfilePicture)
class UserProfilePictureAdmin(admin.ModelAdmin):
    list_display = ["user", "photo"]

@admin.register(pending)
class pendingAdmin(admin.ModelAdmin):
    list_display = ["id_offer", "id_owner", "id_intrested"]
