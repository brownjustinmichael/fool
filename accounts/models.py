import random
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import collections

from polymorphic import PolymorphicModel

from events.models import Event
from cards.models import CardTemplate, CARD_STATUSES, CARD_IN_STASH, CARD_IN_DECK, CARD_IN_DISCARD, CARD_IN_HAND, CARD_IN_PLAY, Deck, Card, BaseCard, PLAYER_STATS, EXTRA_STATS, DEFENSE_BONUS, OFFENSE_BONUS
from results.models import Result

stats = collections.OrderedDict ()
for stat in PLAYER_STATS + EXTRA_STATS:
    stats [stat [0]] = models.IntegerField (default = 0)

class CardStatus (models.Model):
    card = models.ForeignKey (BaseCard)
    deck = models.ForeignKey ('DeckStatus')
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    position = models.IntegerField ()
    played = models.BooleanField (default = False)
    targetDeck = models.ForeignKey ('DeckStatus', blank = True, null = True, default = None, related_name = '_unused_1')
    
    class Meta:
        unique_together = (('deck', 'position', 'status'))
        ordering = ['status', 'position']
        verbose_name_plural = "Card statuses"
        
    def save (self, *args, **kwargs):
        # self.deck = self.card.deck
        return super (CardStatus, self).save (*args, **kwargs)
        
    def draw (self, next_status = CARD_IN_HAND):
        card = self.card.draw (next_status = next_status)
        self.status = next_status
        self.save ()
        return self
        
    def play (self, next_status = CARD_IN_PLAY, played = True):
        value = self.card.play (next_status = next_status)
        self.targetDeck = self.deck
        self.status = next_status
        self.played = played
        self.save ()
        return value
        
    def resolve (self, next_status = CARD_IN_DISCARD):
        self.card.resolve (self.deck.player, self.targetDeck, next_status = next_status)
        if CardStatus.objects.filter (id = self.id).count () > 0:
            self.status = next_status
            self.save ()
        
    def discard (self, next_status = CARD_IN_DISCARD):
        self.card.discard (next_status = next_status)
        self.status = next_status
        self.save ()

class DeckStatus (models.Model):
    player = models.ForeignKey ('Player')
    deck = models.ForeignKey (Deck)
    location = models.ForeignKey ("locations.Location", blank = True, null = True)
    
    class Meta:
        unique_together = (('player', 'deck'))
        verbose_name_plural = "Deck statuses"
        
    def __str__ (self):
        return "%s viewed by %s" % (str (self.deck), str (self.player.user.username))
        
    def save (self, *args, **kwargs):
        try:
            self.location = self.deck.location
        except ObjectDoesNotExist:
            pass
        return super (DeckStatus, self).save (*args, **kwargs)
        
    def addNewCard (self, card, status = CARD_IN_HAND):
        card.deck = self.deck
        card.pk = None
        card.save ()
        if self.getCards (status = status).count () > 0:
            newpos = self.getCards (status = status).last ().position + 1
        else:
            newpos = 0
        cardstatus = CardStatus (card = card, deck = self, status = status, position = newpos)
        cardstatus.save ()
        
    def getNumCards (self, status = CARD_IN_DECK):
        """
        Return the number of cards currently in the deck
        """
        return self.cardstatus_set.filter (status = status).count ()
    
    def getCards (self, **kwargs):
        """
        Return a list of the cards with current status
        """
        status = kwargs.pop ('status', CARD_IN_HAND)
        return self.cardstatus_set.filter (status = status, **kwargs)
        
    def drawCard (self, next_status = CARD_IN_HAND):
        """
        Return the Card instance on top of the deck
        """
        print ("For real this time")
        cardstatus = self.cardstatus_set.filter (status = CARD_IN_DECK).order_by ('position').first ()
        if cardstatus is not None:
            return cardstatus.draw (next_status)
        raise ValueError ("You've run out of cards in this deck.")

    def playCard (self, card, next_status = CARD_IN_HAND):
        """
        Return the Card instance on top of the deck
        """
        return self.cardstatus_set.filter (card = card).first ().play (next_status)
        
    def discard (self, number):
        """Discard the top number cards of the deck"""
        pass

    def reshuffle (self, **kwargs):
        """
        Move the cards in the discard pile to the deck
        """
        
        status = kwargs.pop ('status', None)

        resetCards = []
        if status is None:
            for cardstatus in self.cardstatus_set.filter (**kwargs).all ():
                cardstatus.delete ()
            for card in self.deck.basecard_set.all ():
                if card.isActive ():
                    resetCards.append (card)
        else:
            for cardstatus in self.cardstatus_set.filter (status = status, **kwargs).all ():
                resetCards.append (cardstatus.card)
                cardstatus.delete ()
        
        indices = list (range (len (resetCards)))
        random.shuffle (indices)
        itr = iter (indices)
        for card in resetCards:
            pos = next (itr)
            cardstatus = CardStatus (card = card, status = CARD_IN_DECK, deck = self, position = pos)
            cardstatus.save ()

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
    active_location = models.ForeignKey ("locations.Location", blank = True, null = True)
    
    deck = models.OneToOneField (Deck, null = True, blank = True, related_name = "player")
    
    
    class Meta:
        abstract = True
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
            
    def changeStat (self, stat, value):
        """Change the value of the player's stat by value"""
        setattr (self, stat, getattr (self, stat) + value)
        self.save () 
    
    def recordLog (self, event, result, location):
        Log (title = event.title, event = event, result = result, user = self, location = location).save ()
        
    def playCard (self, card):
        if not isinstance (card, CardStatus):
            cardstatus = card.getStatus (self)
        else:
            cardstatus = card
        if cardstatus.card.template.stat is not None:
            return cardstatus.play () + getattr (self, cardstatus.card.template.stat)
        return cardstatus.play ()
        
    def discard (self, number):
        # TODO Implement this
        print ("Discarding", number, "cards")
        pass
        
    def getCards (self, status = CARD_IN_PLAY):
        return CardStatus.objects.filter (deck__player = self).filter (status = status)
        
    def addDeckStatus (self, deck):
        deckstatus = DeckStatus (deck = deck, player = self)
        deckstatus.save ()
        return deckstatus
        
    def attack (self, npc, scores):
        defenseStat, defenseValue = npc.defend (scores)
        print (defenseStat)
        print (scores)
        damage = -defenseValue
        for stat, value in scores [:]:
            damage += value
            if OFFENSE_BONUS [stat] == defenseStat:
                # TODO Make this more visible to the player, possibly by passing it through score as a modifier
                damage += 1
        if damage >= 0:
            print ("NPC took ", damage)
            npc.discard (damage)
        else:
            print ("You took ", damage)
            self.discard (-damage)
            
    def addEvent (self, cardStatus, event, location):
        event = ActiveEvent (player = self, cardStatus = cardStatus, event = event, stackOrder = self.activeevent_set.count ())
        event.log (location)
        event.save ()
        
    def resolve (self, location, cardStatus = None):
        """Resolve anything unresolved on the stack"""
        lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
        print (self.activeevent_set.order_by ("stackOrder"))
        while lastEvent is not None and lastEvent.resolved:
            if lastEvent.failed:
                lastEvent.log (location)
            lastEvent.delete ()
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
            
        trigger = None
        if lastEvent is not None:
            trigger = lastEvent.resolve (self, location, cardStatus)
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
            
        while lastEvent is not None and lastEvent.resolved:
            if lastEvent.failed:
                lastEvent.log (location)
            lastEvent.delete ()
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
        
        return lastEvent

stats.update ({"__module__": __name__})
Player = type ('Player', (AbstractPlayer,), stats)

class Log (models.Model):
    event = models.ForeignKey (Event)
    failed = models.BooleanField (default = False)
    location = models.ForeignKey ("locations.Location")
    logged = models.DateTimeField (auto_now_add=True)
    
    user = models.ForeignKey (Player)
    
    @property
    def title ():
        return self.event.title
    
    def getContent (self):
        print (self.event.content)
        if self.failed:
            return self.event.generic_content
        else:
            return self.event.content

    content = property (getContent)

    class Meta:
        #Specify the order that the logging messages should appear "logged" for forward and "-logged" for reverse
        ordering = ['logged']
        
    
    
class ActiveEvent (models.Model):
    player = models.ForeignKey (Player)
    event = models.ForeignKey (Event)
    stackOrder = models.IntegerField ()
    cardStatus = models.ForeignKey (CardStatus)
    resolved = models.BooleanField (default = False)
    failed = models.BooleanField (default = False)
    
    class Meta:
        unique_together = ("player", "event", "stackOrder")
        
    def resolve (self, player, location, cardStatus = None):
        trigger, self.failed = self.event.resolve (player, location, cardStatus)
        if trigger is not None and trigger.resolved:
            self.resolved = True
            self.save ()
            
    def log (self, location):
        log = Log (event = self.event, failed = self.failed, user = self.player, location = location)
        log.save ()
