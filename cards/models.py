from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from polymorphic import PolymorphicModel
import abc

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
OFFENSE_BONUS = {FORCE: DASH, DASH: RESIST, RESIST: FORCE, CHARM: CHARM, WISDOM: POWER, POWER: WISDOM}
DEFENSE_BONUS = {FORCE: DASH, DASH: RESIST, RESIST: FORCE, CHARM: CHARM, WISDOM: WISDOM, POWER: POWER}
# ADDITIONAL_DEFENSE = ((CHARM, CHARM_RESIST))

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

class CardTemplate (PolymorphicModel):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    name = models.CharField (max_length = 20)
    requiresTarget = models.BooleanField (default = False)
    
    def __str__ (self):
        return u"%s Template" % self.name
        
    @abc.abstractmethod
    def generateCard (self, **kwargs):
        pass
        
    @abc.abstractmethod
    def _getStat (self):
        pass
        
    def getStat (self):
        return self._getStat ()
        
    stat = property (getStat)
        
class StatTemplate (CardTemplate):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    statistic = models.CharField (max_length = 8, choices = PLAYER_STATS, blank = True)
    
    def generateCard (self, **kwargs):
        return PlayerCard (template = self, **kwargs)
        
    def _getStat (self):
        print ("CALLING XSTAT STAT")
        print (self.statistic)
        return self.statistic
    
class ItemTemplate (CardTemplate):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    statistic = models.CharField (max_length = 8, choices = PLAYER_STATS, blank = True)
    
    def generateCard (self, **kwargs):
        return ItemCard (template = self, **kwargs)
        
    def _getStat (self):
        print ("CALLING XSTAT ITEM")
        
        return self.statistic
        
class NPCTemplate (CardTemplate):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    npc = models.ForeignKey ("npcs.NPC")
    
    def generateCard (self, **kwargs):
        return NPCCard (template = self, **kwargs)
        
    def _getStat (self):
        print ("CALLING XSTAT NPC")
        return None

class Deck (models.Model):
    # TODO Almost every method of this class is redundant with those of DeckStatus
    
    def getStatus (self, player, **kwargs):
        """
        If there's a deckStatus object associated with this deck and player, return it; otherwise, make one and return that
        """
        deckstatus = self.deckstatus_set.filter (player = player).first ()
        if deckstatus is None:
            deckstatus = player.addDeckStatus (self)
            # deckstatus.initialize (**kwargs)
        return deckstatus
    
    def getNumCards (self, player, status = CARD_IN_DECK):
        """
        Return the number of cards currently in the deck
        """
        return self.getStatus (player).getNumCards (status)

    def getCards (self, player, status = CARD_IN_HAND):
        """
        Return a list of the cards with current status
        """
        return self.getStatus (player).getCards (status)

    def drawCard (self, player):
        """
        Return the Card instance on top of the deck
        """
        print ("I'm drawing a card...")
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

class BaseCard (PolymorphicModel):
    """
    This is a playable instance of the cardtemplate class. It should contain methods for card use, upgrades, socketing, etc.
    """
    modifier = models.IntegerField ()
    description = models.TextField (blank = True, null = True)
    deck = models.ForeignKey (Deck, null = True, blank = True)
    
    def __str__ (self):
        return u"%s %d" % (self.getTemplate (), self.modifier)
        
    def isActive (self):
        return True
        
    @abc.abstractmethod
    def getTemplate (self):
        pass
        
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
        
    def resolve (self, player, targetDeck = None, next_status = CARD_IN_DISCARD):
        for effectlink in self.getTemplate ().effectlink_set.all ():
            effectlink.effect.affect (self.modifier, player, targetDeck)
        return self
        
    def discard (self, next_status = CARD_IN_DISCARD):
        self.status = next_status
        self.save ()
        
class Card (BaseCard):
    template = models.ForeignKey (CardTemplate)
    
    def getTemplate (self):
        return self.template
    
class PlayerCard (BaseCard):
    template = models.ForeignKey (StatTemplate)
    experience = models.IntegerField (default = 0)
    
    def __str__ (self):
        return u"%s %d w/ EXP %d" % (self.template, self.modifier, self.experience)
        
    def getTemplate (self):
        return self.template
    
    def resolve (self, player, targetDeck = None, next_status = CARD_IN_DISCARD):
        # TODO Player Cards shouldn't gain experience when played outside of context
        self.experience += 1
        self.save ()
        return super (PlayerCard, self).resolve (player, targetDeck, next_status)
        
class ItemCard (BaseCard):
    template = models.ForeignKey (ItemTemplate)
    
    def __str__ (self):
        return u"%s %d" % (self.template, self.modifier)
        
    def getTemplate (self):
        return self.template
        
    def resolve (self, player, targetDeck = None, next_status = CARD_IN_DISCARD):
        if self.getStatus (player).played:
            result = super (ItemCard, self).resolve (player, targetDeck, next_status)
            self.delete ()

class NPCCard (BaseCard):
    """
    An NPC Card is a representation of an NPC that, when played, adds an interaction with the NPC onto the stack
    """
    template = models.ForeignKey (NPCTemplate)
    
    def __str__ (self):
        return u"%s %d" % (self.template, self.modifier)
        
    def getTemplate (self):
        return self.template
    

class Effect (PolymorphicModel):
    name = models.CharField (max_length = 60, default = "Effect")
    
    # class Meta:
    #     abstract = True
        
    @abc.abstractmethod
    def affect (self, multiplier, player, targetDeck):
        pass
        
    def __str__ (self):
        return self.name
    
class HealEffect (Effect):
    def affect (self, multiplier, player, targetDeck):
        if isinstance (targetDeck, Deck):
            targetDeck = targetDeck.getStatus (player)
        if targetDeck is not None:
            for cardstatus in targetDeck.getCards (status = CARD_IN_DISCARD).order_by ('-position') [:min (multiplier, targetDeck.getNumCards (CARD_IN_DISCARD))]:
                cardstatus.status = CARD_IN_DECK
                cardstatus.save ()
        # status.reshuffle (status = CARD_IN_DECK)
        
class StatusChangeEffect (Effect):
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS)
    strength = models.IntegerField (default = 0)
    
    def __str__ (self):
        return self.stat + " " + self.strength
    
    def affect (self, multiplier, player, targetDeck):
        player.changeStat (self.stat, self.strength)
        
class EffectLink (models.Model):
    template = models.ForeignKey (CardTemplate)
    effect = models.ForeignKey (Effect)