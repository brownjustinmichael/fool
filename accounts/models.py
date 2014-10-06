import random
from django.db import models
from django.contrib.auth.models import User

import collections

from events.models import Event
from locations.models import Location
from cards.models import CardTemplate, CARD_STATUSES, CARD_IN_STASH, CARD_IN_DECK, CARD_IN_DISCARD, CARD_IN_HAND, CARD_IN_PLAY, Deck, Card, PLAYER_STATS, EXTRA_STATS
from results.models import Result

stats = collections.OrderedDict ()
for stat in PLAYER_STATS + EXTRA_STATS:
    stats [stat [0]] = models.IntegerField (default = 0)

class CardStatus (models.Model):
    card = models.ForeignKey (Card)
    deck = models.ForeignKey ('DeckStatus')
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    position = models.IntegerField ()
    
    class Meta:
        unique_together = (('deck', 'position', 'status'))
        ordering = ['status', 'position']
        
    def save (self, *args, **kwargs):
        # self.deck = self.card.deck
        return super (CardStatus, self).save (*args, **kwargs)
        
    def draw (self, next_status = CARD_IN_HAND):
        card = self.card.draw (next_status = next_status)
        self.status = next_status
        self.save ()
        return card
        
    def play (self, next_status = CARD_IN_PLAY):
        value = self.card.play (next_status = next_status)
        self.status = next_status
        self.save ()
        return value
        
    def resolve (self, next_status = CARD_IN_DISCARD):
        self.card.resolve (next_status = next_status)
        self.status = next_status
        self.save ()    
        
    def discard (self, next_status = CARD_IN_DISCARD):
        self.card.discard (next_status = next_status)
        self.status = next_status
        self.save ()

class DeckStatus (models.Model):
    player = models.ForeignKey ('Player')
    deck = models.ForeignKey (Deck)
    
    class Meta:
        unique_together = (('player', 'deck'))
        
    def getNumCards (self, status = CARD_IN_DECK):
        """
        Return the number of cards currently in the deck
        """
        return self.cardstatus_set.filter (status = status).count ()
    
    def getCards (self, status):
        """
        Return a list of the cards with current status
        """
        return self.cardstatus_set.filter (status = status)
        
    def drawCard (self, next_status = CARD_IN_HAND):
        """
        Return the Card instance on top of the deck
        """
        return self.cardstatus_set.filter (status = CARD_IN_DECK).order_by ('position').first ().draw (next_status)

    def playCard (self, card, next_status = CARD_IN_HAND):
        """
        Return the Card instance on top of the deck
        """
        return self.cardstatus_set.filter (card = card).first ().play (next_status)

    def reshuffle (self):
        """
        Move the cards in the discard pile to the deck
        """
        for cardstatus in self.cardstatus_set.all ():
            cardstatus.delete ()
        indices = list (range (self.deck.card_set.count ()))
        random.shuffle (indices)
        itr = iter (indices)
        for card in self.deck.card_set.all ():
            if card.isActive ():
                pos = next (itr)
                print (pos)
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
    active_location = models.ForeignKey (Location, blank = True, null = True)
    
    deck = models.OneToOneField (Deck, null = True, blank = True, related_name = "player")
    
    
    class Meta:
        abstract = True
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
            
    def recordLog (self, event, result, location):
        Log (title = event.title, event = event, result = result, user = self, location = location).save ()
        
    def playCard (self, card):
        cardstatus = card.getStatus (self)
        if card.template.stat is not None:
            return cardstatus.play () + getattr (self, card.template.stat)
        return cardstatus.play ()
        
    def addDeckStatus (self, deck):
        deckstatus = DeckStatus ()

stats.update ({"__module__": __name__})
Player = type ('Player', (AbstractPlayer,), stats)

class Log (models.Model):
    title = models.CharField (max_length = 255)
    event = models.ForeignKey (Event)
    result = models.ForeignKey (Result)
    location = models.ForeignKey (Location)
    logged = models.DateTimeField (auto_now_add=True)
    
    user = models.ForeignKey (Player)
    
    class Meta:
        #Specify the order that the logging messages should appear "logged" for forward and "-logged" for reverse
        ordering = ['logged']
        
