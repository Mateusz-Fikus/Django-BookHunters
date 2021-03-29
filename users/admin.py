from django.contrib import admin
from users.models import User, UserProfilePicture

@admin.register(User)
class UserAdminSite(admin.ModelAdmin):
    list_display = ["email", "username"]

@admin.register(UserProfilePicture)
class UserProfilePictureAdmin(admin.ModelAdmin):
    list_display = ["user", "photo"]
