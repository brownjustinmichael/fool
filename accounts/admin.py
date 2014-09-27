from django.contrib import admin
from accounts.models import Player, Card

class CardInline(admin.TabularInline):
    model = Card

class PlayerAdmin (admin.ModelAdmin):
    inlines = [
        CardInline,
    ]

admin.site.register(Player, PlayerAdmin)
admin.site.register (Card)