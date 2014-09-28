from django.contrib import admin
from accounts.models import Player, Card, Deck
from django.core.urlresolvers import reverse

class CardInline(admin.TabularInline):
    model = Card

class DeckInline(admin.TabularInline):
    model = Deck
    
class PlayerAdmin (admin.ModelAdmin):
    # raw_id_fields = ('deck',)
    # related_lookup_fields = { 'deck': ['deck'],}
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'script.js',       # project static folder
        )
    
class DeckAdmin (admin.ModelAdmin):
    inlines = [
        CardInline,
    ]

# admin.site.register(Player)
admin.site.register(Player, PlayerAdmin)
admin.site.register (Card)
admin.site.register (Deck, DeckAdmin)