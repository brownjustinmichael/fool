from django.contrib import admin
from accounts.models import Player, CardAttribute

class CardAttributeInline(admin.TabularInline):
    model = CardAttribute

class PlayerAdmin (admin.ModelAdmin):
    inlines = [
        CardAttributeInline,
    ]

admin.site.register(Player, PlayerAdmin)
admin.site.register (CardAttribute)