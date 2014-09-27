from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import collections
import random

from events.models import Event
from locations.models import Location
from cards.models import CardTemplate, PLAYER_STATS

CARD_IN_HAND = "hand"
CARD_IN_DECK = "deck"
CARD_IN_DISCARD = "discard"
CARD_IN_STASH = "stash"
CARD_STATUSES = ((CARD_IN_HAND, "Hand"), (CARD_IN_DECK, "Deck"), (CARD_IN_DISCARD, "Discard"), (CARD_IN_STASH, "Stash"))

stats = collections.OrderedDict ()
for stat in PLAYER_STATS:
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
        return self.card_set.filter (status = CARD_IN_DECK).count ()
    
    def getCardsInHand (self):
        """
        Return a list of the cards currently in the player's hand
        """
        return filter (lambda x: x.status == CARD_IN_HAND, self.card_set.all ())
        
    def drawCard (self):
        """
        Return the Card instance on top of the deck
        """
        random_index = random.randint(0, self.getNumCardsInDeck () - 1)
        return self.card_set.filter (status = CARD_IN_DECK).all () [random_index]

    def reshuffle (self):
        """
        Move the cards in the discard pile to the deck
        """
        for card in self.card_set.filter (status = CARD_IN_DISCARD).all ():
            card.status = CARD_IN_DECK
            card.save ()

stats.update ({"__module__": __name__})
Player = type ('Player', (AbstractPlayer,), stats)

class Card (models.Model):
    """
    This is a usable instance of the cardtemplate class. It should contain methods for card use, upgrades, socketing, etc.
    """
    modifier = models.IntegerField ()
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    
    player = models.ForeignKey (Player)
    template = models.ForeignKey (CardTemplate)
    
    def __str__ (self):
        return u"%s's %s" % (self.player.user, self.card)
        
    def get_absolute_url (self):
        return reverse ('cards.views.card', args=[self.id])
    
    def play (self):
        """
        If playing the card would have a strange effect or unique bonuses, that effect should go here in a subclass
        """
        self.status = CARD_IN_DISCARD
        if self.template.stat != None:
            return self.modifier + getattr (self.player, self.template.stat)
        return self.modifier
