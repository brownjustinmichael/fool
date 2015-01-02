import random
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from polymorphic import PolymorphicModel

import abc

import collections

from polymorphic import PolymorphicModel

from events.models import Event, EventTrigger
from locations.models import Location
from cards.models import CardTemplate, CARD_STATUSES, CARD_IN_STASH, CARD_IN_DECK, CARD_IN_DISCARD, CARD_IN_HAND, CARD_IN_PLAY, Deck, Card, BaseCard, PLAYER_STATS, EXTRA_STATS, DEFENSE_BONUS, OFFENSE_BONUS, RESIST, FORCE

stats = collections.OrderedDict ()
for stat in PLAYER_STATS + EXTRA_STATS:
    stats [stat [0]] = models.IntegerField (default = 0)

class CardStatus (models.Model):
    """
    A CardStatus object is an instance of a Card object
    """
    card = models.ForeignKey (BaseCard)
    deck = models.ForeignKey ('DeckStatus', null = True, blank = True)
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    position = models.IntegerField ()
    played = models.BooleanField (default = False)
    targetDeck = models.ForeignKey ('DeckStatus', blank = True, null = True, default = None, related_name = '_unused_1')
    
    class Meta:
        unique_together = (('deck', 'position', 'status'))
        ordering = ['status', 'position']
        verbose_name_plural = "Card statuses"
        
    def save (self, *args, **kwargs):
        """
        Saves the object to the database
        """
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
    initialized = models.BooleanField (default = False)
    
    class Meta:
        unique_together = (('player', 'deck'))
        verbose_name_plural = "Deck statuses"
        
    def __str__ (self):
        return "%s viewed by %s" % (str (self.deck), str (self.player.user.username))
        
    def checkInitialize (self):
        if not self.initialized:
            self.initialize ()
        
    def initialize (self):
        resetCards = []
        for card in self.deck.basecard_set.all ():
            if card.isActive ():
                resetCards.append (card)
        
        indices = list (range (len (resetCards)))
        random.shuffle (indices)
        itr = iter (indices)
        for card in resetCards:
            pos = next (itr)
            cardstatus = CardStatus (card = card, status = CARD_IN_DECK, deck = self, position = pos)
            cardstatus.save ()
        
        self.initialized = True
        self.save ()
        
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
        self.checkInitialize ()
        return self.cardstatus_set.filter (status = status).count ()
    
    def getCards (self, **kwargs):
        """
        Return a list of the cards with current status
        """
        self.checkInitialize ()
        status = kwargs.pop ('status', CARD_IN_HAND)
        return self.cardstatus_set.filter (status = status, **kwargs)
        
    def drawCard (self, next_status = CARD_IN_HAND, force = False):
        """
        Return the CardStatus instance on top of the deck and set that card's status to next_status
        
        This method will raise an error if a card is attempted to be drawn from an empty deck or if there is an unresolved event
        
        next_status: The next status for the card drawn, by default CARD_IN_HAND
        force: If a card should be drawn regardless of whether there are events in play (e.g. an item card that lets the player draw), set force to True
        
        return: The CardStatus object drawn from the deck
        """
        self.checkInitialize ()
        if not force and self.player.active_event is not None:
            raise RuntimeError ("You can't draw from a deck if there's an unresolved event on the stack")
        
        cardstatus = self.cardstatus_set.filter (status = CARD_IN_DECK).order_by ('position').first ()
        if cardstatus is not None:
            return cardstatus.draw (next_status)
        raise ValueError ("You've run out of cards in this deck.")

    def playCard (self, card, next_status = CARD_IN_HAND):
        """
        Return the Card instance on top of the deck
        """
        self.checkInitialize ()
        return self.cardstatus_set.filter (card = card).first ().play (next_status)
        
    def discard (self, number, next_status = CARD_IN_DISCARD):
        """Discard the top number cards of the deck"""
        self.checkInitialize ()
        for i in range (number):
            cardstatus = self.cardstatus_set.filter (status = CARD_IN_DECK).order_by ('position').first ()
            if cardstatus is not None:
                return cardstatus.discard (next_status)
        raise ValueError ("You've run out of cards in this deck.")
        
    def reshuffle (self, **kwargs):
        """
        Move the cards in the discard pile to the deck
        """
        
        if self.player.active_event is not None:
            raise RuntimeError ("You can't shuffle a deck if there's an unresolved event on the stack")
        
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
        
        self.initialized = False
        self.delete ()
        self.save ()

class AbstractPlayer (models.Model):
    """
    This object contains the critical information about the player needed to play the game. These include:
        user: A link to the user object associated with the player
        active_event: A link to the event object that's currently active
        active_location: A link to the location where the current event is active
        stats: A set of integer stat fields specified in USER_STATS
    """
    user = models.OneToOneField (User)
    deck = models.OneToOneField (Deck, null = True, blank = True, related_name = "player")
    
    class Meta:
        abstract = True
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
        
    def getActiveEvent (self):
        return self.activeevent_set.order_by ("stackOrder").last ()
        
    active_event = property (getActiveEvent)
    
    def getActiveEvents (self):
        return self.activeevent_set.order_by ("stackOrder").all ()
        
    active_events = property (getActiveEvents)
    
    
    def getActiveLocation (self):
        active = self.active_event
        if active is not None:
            return active.location
        else:
            return None
            
    active_location = property (getActiveLocation)
            
    def changeStat (self, stat, value):
        """Change the value of the player's stat by value"""
        setattr (self, stat, getattr (self, stat) + value)
        self.save () 
    
    def recordLog (self, event, result, location):
        Log (title = event.title, event = event, result = result, user = self, location = location).save ()
        
    def maxCardsInHand (self):
        return getattr (self, RESIST)
        
    handMax = property (maxCardsInHand)
        
    def maxCardsInDeck (self):
        return getattr (self, FORCE) * 4
        
    def draw (self):
        """
        Draw cards until your hand is full
        """
        if (self.getCards (CARD_IN_HAND).count () >= self.maxCardsInHand ()):
            raise RuntimeError ("You can't exceed the maximum number of cards in your hand")
        while self.getCards (CARD_IN_HAND).count () < self.maxCardsInHand ():
            self.deck.getStatus (self).drawCard ()
        
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
        self.deck.getStatus (self).discard (number)
        
    def reshuffleAll (self):
        for deckStatus in self.deckstatus_set.all ():
            deckStatus.reshuffle ()
        
    def getCards (self, status = CARD_IN_PLAY):
        return CardStatus.objects.filter (deck__player = self).filter (status = status)
        
    def addDeckStatus (self, deck):
        deckstatus = DeckStatus (deck = deck, player = self)
        deckstatus.save ()
        return deckstatus
        
    def attack (self, npc, scores):
        defenseStat, defenseValue = npc.defend (scores)
        if defenseValue < 0:
            print ("Immune")
            return
        if scores [0] [0] == RESIST:
            print ("You can't attack with resist")
            return
        print (defenseStat)
        print (scores)
        damage = -defenseValue
        for stat, value in scores [:]:
            damage += value
            if OFFENSE_BONUS [stat] == defenseStat:
                # TODO Make this more visible to the player, possibly by passing it through score as a modifier
                # damage += 1
                pass
        if damage >= 0:
            print ("NPC took ", damage)
            npc.discard (damage)
        else:
            print ("You took ", damage)
            self.discard (-damage)
            
    def addEvent (self, cardStatus, event, location):
        """
        Add an active event to the event stack using the cardstatus as the appropriate card for that event
        
        cardStatus: a CardStatus object to associate with the new event
        event: an Event object to add to the event stack
        location: the Location object that identifies where the event takes place
        """
        event = ActiveEvent (player = self, cardStatus = cardStatus, event = event, stackOrder = self.activeevent_set.count (), location = location)
        event.log ()
        event.save ()
        
    def resolve (self, location, cardStatus = None):
        """
        Resolve anything unresolved on the stack.
        
        This first checks for any unresolved events on the stack. Then, if there are still events on the stack, it attempts to trigger a new event. At the end, it checks again for any unresolved events and resolves any free cards in play that aren't associated with events.
        
        location: The Location object where the resolution is taking place
        cardStatus: If a card was played this turn, it would get passed here. If no card was played, this is None
        
        returns: The topmost ActiveEvent object on the stack
        """
        
        # Check for unresolved events on the stack
        lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
        while lastEvent is not None and lastEvent.resolved:
            if lastEvent.failed:
                lastEvent.log ()
            lastEvent.delete ()
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
            
        # Attempt to trigger a new event using any cards that may have been played
        if lastEvent is not None:
            trigger, failed = lastEvent.resolve (self, location, cardStatus)
            if trigger is not None:
                log = TriggerLog (trigger = trigger, user = self, location = location, success = not failed)
                log.save ()
                if not failed:
                    self.addEvent (cardStatus = cardStatus, event = trigger.event, location = location)
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
            
        # Check for unresolved events on the stack
        while lastEvent is not None and lastEvent.resolved:
            if lastEvent.failed:
                lastEvent.log ()
            lastEvent.delete ()
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
        
        # Resolve any free cards in play
        for card in self.getCards (CARD_IN_PLAY):
            try:
                if card.activeEvent is None:
                    card.resolve ()
            except ObjectDoesNotExist:
                card.resolve ()
                
        # Return the current event
        return lastEvent

# An actual player instance needs everything from the AbstractPlayer class but also a set of stats, which we define here dynamically in case we need to add more and to reduce redundancy between this and the CardTemplate classes
stats.update ({"__module__": __name__})
Player = type ('Player', (AbstractPlayer,), stats)

class Log (PolymorphicModel):
    event = models.ForeignKey (Event, null =  True, blank = True)
    location = models.ForeignKey ("locations.Location")
    logged = models.DateTimeField (auto_now_add=True)
    
    user = models.ForeignKey (Player)
    
    @property
    def title ():
        return self.event.title
    
    def getContent (self):
        return self.event.content

    content = property (getContent)

    class Meta:
        #Specify the order that the logging messages should appear "logged" for forward and "-logged" for reverse
        ordering = ['logged']
        
class TriggerLog (Log):
    trigger = models.ForeignKey (EventTrigger)
    success = models.BooleanField (default = True)
    
    @property
    def title ():
        return self.trigger.title
    
    def getContent (self):
        if self.success:
            return self.trigger.content
        return self.trigger.failed_content
    
    content = property (getContent)
    
class ActiveEvent (models.Model):
    player = models.ForeignKey (Player)
    event = models.ForeignKey (Event)
    stackOrder = models.IntegerField ()
    cardStatus = models.OneToOneField (CardStatus, related_name = "activeEvent")
    resolved = models.BooleanField (default = False)
    failed = models.BooleanField (default = False)
    location = models.ForeignKey (Location, null = True)
    
    class Meta:
        unique_together = ("player", "event", "stackOrder")
        
    def getLife (self):
        if self.event.life is not None:
            return self.event.life + self.event.generateNPCInstance (self.player).life
            
    life = property (getLife)
        
    def resolve (self, player, location, cardStatus = None):
        trigger, self.failed = self.event.resolve (player, location, cardStatus)
        if trigger is not None and not self.failed and trigger.resolved:
            self.resolved = True
            self.save ()
        return trigger, self.failed
            
    def log (self):
        log = Log (event = self.event, user = self.player, location = self.location)
        log.save ()
