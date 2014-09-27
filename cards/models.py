from django.db import models
from django.core.urlresolvers import reverse

CARD_IN_HAND = "hand"
CARD_IN_DECK = "deck"
CARD_IN_DISCARD = "discard"
CARD_IN_STASH = "stash"
CARD_STATUSES = ((CARD_IN_HAND, "Hand"), (CARD_IN_DECK, "Deck"), (CARD_IN_DISCARD, "Discard"), (CARD_IN_STASH, "Stash"))

FORCE = "force"
DASH = "dash"
RESIST = "resist"
CHARM = "charm"
WISDOM = "wisdom"
POWER = "power"
MONEY = "money"
PLAYER_STATS = ((FORCE, "Force"), (DASH, "Dash"), (RESIST, "Resist"), (CHARM, "Charm"), (WISDOM, "Wisdom"), (POWER, "Power"), (MONEY, "Money"))

class CardTemplate (models.Model):
    # This field is required.
    name = models.CharField (max_length = 20)
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS, blank = True)
    
    def __str__ (self):
        return u"%s" % self.name
