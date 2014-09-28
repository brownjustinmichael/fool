from django.contrib import admin
from cards.models import CardTemplate, Card, Deck

class CardInline(admin.TabularInline):
    model = Card

class DeckInline(admin.TabularInline):
    model = Deck
    
class DeckAdmin (admin.ModelAdmin):
    inlines = [
        CardInline,
    ]
    
admin.site.register (Card)
admin.site.register (Deck, DeckAdmin)
admin.site.register (CardTemplate)
