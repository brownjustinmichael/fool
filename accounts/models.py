from django.db import models
from django.contrib.auth.models import User

import collections
import random

from events.models import Event
from locations.models import Location
from cards.models import Card

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
USER_STATS = ((FORCE, "Force"), (DASH, "Dash"), (RESIST, "Resist"), (CHARM, "Charm"), (WISDOM, "Wisdom"), (POWER, "Power"), (MONEY, "Money"))

stats = collections.OrderedDict ()
for stat in USER_STATS:
    stats [stat [0]] = models.IntegerField (default = 0)
print (stats)

class AbstractPlayer (models.Model):
    """
    This object contains the critical information about the player needed to play the game. These include:
        user: A link to the user object associated with the player
        active_event: A link to the event object that's currently active
        active_location: A link to the location where the current event is active
        stats: A set of integer stat fields specified in USER_STATS
    """
    user = models.OneToOneField (User)

    active_event = models.ForeignKey (Event, blank = True, null = True)
    active_location = models.ForeignKey (Location, blank = True, null = True)
    
    class Meta:
        abstract = True
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
        
    def getNumCardsInDeck (self):
        """
        Return the number of cards currently in the deck
        """
        return self.cardattribute_set.filter (status = CARD_IN_DECK).count ()
    
    def getCardsInHand (self):
        """
        Return a list of the cards currently in the player's hand
        """
        return filter (lambda x: x.status == CARD_IN_HAND, self.cardattribute_set.all ())
        
    def drawCard (self):
        """
        Return the Card instance on top of the deck
        """
        random_index = random.randint(0, self.getNumCardsInDeck () - 1)
        return self.cardattribute_set.filter (status = CARD_IN_DECK).all () [random_index]

    def reshuffle (self):
        """
        Move the cards in the discard pile to the deck
        """
        for card in self.cardattribute_set.filter (status = CARD_IN_DISCARD).all ():
            card.status = CARD_IN_DECK
            card.save ()

stats.update ({"__module__": __name__})
Player = type ('Player', (AbstractPlayer,), stats)

class CardAttribute (models.Model):
    player = models.ForeignKey (Player)
    card = models.ForeignKey (Card)
    modifier = models.IntegerField ()
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    
    def __str__ (self):
        return u"%s's %s" % (self.player.user, self.card)
        
    def get_absolute_url (self):
        return reverse ('cards.views.card', args=[self.id])
        
