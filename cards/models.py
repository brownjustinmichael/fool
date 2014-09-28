from django.db import models
from django.core.urlresolvers import reverse

import random

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
PLAYER_STATS = ((FORCE, "Force"), (DASH, "Dash"), (RESIST, "Resist"), (CHARM, "Charm"), (WISDOM, "Wisdom"), (POWER, "Power"))

MONEY = "money"
EXTRA_STATS = ((MONEY, "Money"),)

class CardTemplate (models.Model):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    name = models.CharField (max_length = 20)
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS, blank = True)
    
    def __str__ (self):
        return u"%s Template" % self.name

class Deck (models.Model):
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
        
class Card (models.Model):
    """
    This is a playable instance of the cardtemplate class. It should contain methods for card use, upgrades, socketing, etc.
    """
    modifier = models.IntegerField ()
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    
    deck = models.ForeignKey (Deck)
    template = models.ForeignKey (CardTemplate)
    
    def __str__ (self):
        return u"%s's %s %d" % ("FIX", self.template, self.modifier)
        
    def get_absolute_url (self):
        return reverse ('cards.views.card', args=[self.id])
    
    def play (self):
        """
        If playing the card would have a strange effect or unique bonuses, that effect should go here in a subclass
        """
        self.status = CARD_IN_DISCARD
        self.save ()
        return self.modifier