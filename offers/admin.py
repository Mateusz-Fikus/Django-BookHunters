from django.contrib import admin
from offers.models import offer, pending


@admin.register(offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["id_owner_user", "title", "id_buyer"]


class pendingAdmin(admin.ModelAdmin):
    list_display = ["id_offer", "id_owner", "id_intrested"]
