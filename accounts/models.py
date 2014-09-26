from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from locations.models import Location
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
MONEY = "money"
USER_STATS = ((FORCE, "Force"), (DASH, "Dash"), (RESIST, "Resist"), (CHARM, "Charm"), (WISDOM, "Wisdom"), (POWER, "Power"), (MONEY, "Money"))

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField (User)

    # Other fields here
    accepted_eula = models.BooleanField(default = False)
    favorite_animal = models.CharField(max_length=20, default="Dragons")
    active_event = models.ForeignKey (Event, blank = True, null = True)
    active_location = models.ForeignKey (Location, blank = True, null = True)
    
    force = models.IntegerField (default = 0)
    dash = models.IntegerField (default = 0)
    resist = models.IntegerField (default = 0)
    charm = models.IntegerField (default = 0)
    wisdom = models.IntegerField (default = 0)
    power = models.IntegerField (default = 0)
    
    money = models.IntegerField (default = 0)
        
    def __str__ (self):
        return u"%s's Profile" % self.user.username
        
    def getCardsInHand (self):
        return filter (lambda x: x.status == CARD_IN_HAND, self.cardattribute_set.all ())
        
    def drawCard (self):
        random_index = random.randint(0, self.getNumCardsInDeck () - 1)
        return self.cardattribute_set.filter (status = CARD_IN_DECK).all () [random_index]

    def getNumCardsInDeck (self):
        return self.cardattribute_set.filter (status = CARD_IN_DECK).count ()

    def reshuffle (self):
        for card in self.cardattribute_set.filter (status = CARD_IN_DISCARD).all ():
            card.status = CARD_IN_DECK
            card.save ()
