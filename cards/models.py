from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

import random

CARD_IN_HAND = "hand"
CARD_IN_DECK = "deck"
CARD_IN_DISCARD = "discard"
CARD_IN_STASH = "stash"
CARD_IN_PLAY = "play"
CARD_STATUSES = ((CARD_IN_HAND, "Hand"), (CARD_IN_DECK, "Deck"), (CARD_IN_DISCARD, "Discard"), (CARD_IN_STASH, "Stash"), (CARD_IN_PLAY, "Play"))

FORCE = "force"
DASH = "dash"
RESIST = "resist"
CHARM = "charm"
WISDOM = "wisdom"
POWER = "power"
PLAYER_STATS = ((FORCE, "Force"), (DASH, "Dash"), (RESIST, "Resist"), (CHARM, "Charm"), (WISDOM, "Wisdom"), (POWER, "Power"))

MONEY = "money"
EXTRA_STATS = ((MONEY, "Money"),)

class Score (object):
    def __init__ (self, stat = None, value = 0):
        self.stat = stat
        self.value = value
        
    def __add__ (self, score):
        if (isinstance (score, Score)):
            if (score.stat != self.stat):
                raise TypeError
            return Score (self.stat, self.value + score.value)
        else:
            return Score (self.stat, self.value + score)
            
    def __sub__ (self, score):
        if (isinstance (score, Score)):
            if (score.stat != self.stat):
                raise TypeError
            return Score (self.stat, self.value - score.value)
        else:
            return Score (self.stat, self.value - score)
            
    def __mul__ (self, score):
        return Score (self.stat, self.value * score)
        
    def __div__ (self, score):
        return Score (self.stat, self.value / score)
        
    def __iter__ (self):
        return iter ((self.stat, self.value))

class CardTemplate (models.Model):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    name = models.CharField (max_length = 20)
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS, blank = True)
    
    def __str__ (self):
        return u"%s Template" % self.name

class Deck (models.Model):
    def getStatus (self, player):
        deckstatus = self.deckstatus_set.filter (player = player).first ()
        if deckstatus is None:
            deckstatus = player.addDeckStatus (self)
        print (deckstatus)
        return deckstatus
    
    def getNumCards (self, player, status = CARD_IN_DECK):
        """
        Return the number of cards currently in the deck
        """
        return self.getStatus (player).getNumCards ()
    
    def getCards (self, player, status = CARD_IN_HAND):
        """
        Return a list of the cards with current status
        """
        return self.getStatus (player).getCards (status)
        
    def drawCard (self, player):
        """
        Return the Card instance on top of the deck
        """
        return self.getStatus (player).drawCard ()
        
    def playCard (self, player, card):
        """
        Return the Card instance on top of the deck
        """
        return self.getStatus (player).playCard (card)

    def reshuffle (self, player):
        """
        Move the cards in the discard pile to the deck
        """
        self.getStatus (player).reshuffle ()
            
    def __str__ (self):
        try:
            if self.player is not None:
                return "%s's Deck" % (str (self.player.user.username))
        except ObjectDoesNotExist:
            pass
        try:
            if self.location is not None:
                return "Deck at %s" % (str (self.location))
        except ObjectDoesNotExist:
            pass
        return "Unattached Deck"
            
class Card (models.Model):
    """
    This is a playable instance of the cardtemplate class. It should contain methods for card use, upgrades, socketing, etc.
    """
    modifier = models.IntegerField ()
    
    deck = models.ForeignKey (Deck)
    template = models.ForeignKey (CardTemplate)
    
    def __str__ (self):
        return u"%s %d" % (self.template, self.modifier)
        
    def isActive (self):
        return True
        
    def getStatus (self, player):
        return self.cardstatus_set.filter (deck = self.deck.getStatus (player)).first ()
        
    def get_absolute_url (self):
        return reverse ('cards.views.card', args=[self.id])
        
    def draw (self, next_status = CARD_IN_HAND):
        return self
    
    def play (self, next_status = CARD_IN_PLAY):
        """
        If playing the card would have a strange effect or unique bonuses, that effect should go here in a subclass
        """
        return Score (self.template.stat, self.modifier)
        
    def discard (self, next_status = CARD_IN_DISCARD):
        self.status = next_status
        self.save ()