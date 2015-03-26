from accounts.models import CardStatus

from accounts.models import Player

Player.objects.filter (user__username = "justinbrown")
me = Player.objects.filter (user__username = "justinbrown") [0]

from cards.models import Card

from cards.models import Deck

decks = Deck.objects.all ()

deck = decks [13]

from accounts.models import CARD_IN_DECK

from cards.models import NPCTemplate
from npcs.models import NPC

bookcasenpc = NPC.objects.filter (name = "Bookcase")

booktemplate = NPCTemplate.objects.filter (npc = bookcasenpc).first ()

cards = deck.getCards (me, CARD_IN_DECK)

for card in cards:
    print (card)
    if card.card.template == booktemplate:
        bookcase = card
        break

me.resolve (me.active_location, bookcase)
