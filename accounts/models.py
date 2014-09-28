from django.db import models
from django.contrib.auth.models import User

import collections

from events.models import Event
from locations.models import Location
from cards.models import CardTemplate, Deck, PLAYER_STATS, EXTRA_STATS
from results.models import Result

stats = collections.OrderedDict ()
for stat in PLAYER_STATS + EXTRA_STATS:
    stats [stat [0]] = models.IntegerField (default = 0)

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
    
    deck = models.OneToOneField (Deck, null = True, blank = True)
    
    class Meta:
        abstract = True
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
            
    def recordLog (self, event, result, location):
        Log (title = event.title, event = event, result = result, user = self, location = location).save ()
        
    def playCard (self, card):
        if card.template.stat is not None:
            return card.play () + getattr (self, card.template.stat)
        return card.play ()

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