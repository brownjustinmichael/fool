from django.db import models
from django.contrib.auth.models import User
from scenarios.models import Scenario
from locations.models import Location

CARD_IN_HAND = "hand"
CARD_IN_DECK = "deck"
CARD_IN_DISCARD = "discard"
CARD_IN_STASH = "stash"
CARD_STATUSES = ((CARD_IN_HAND, "Hand"), (CARD_IN_DECK, "Deck"), (CARD_IN_DISCARD, "Discard"), (CARD_IN_STASH, "Stash"))

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField (User)

    # Other fields here
    accepted_eula = models.BooleanField(default = False)
    favorite_animal = models.CharField(max_length=20, default="Dragons")
    active_scenario = models.ForeignKey (Scenario, blank = True, null = True)
    active_location = models.ForeignKey (Location, blank = True, null = True)
    
    force = models.IntegerField (default = 0)
    dash = models.IntegerField (default = 0)
    resist = models.IntegerField (default = 0)
    charm = models.IntegerField (default = 0)
    wisdom = models.IntegerField (default = 0)
    power = models.IntegerField (default = 0)
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
        
    def getCardsInHand (self):
        return filter (lambda x: x.status == CARD_IN_HAND, self.cardattributes_set.all ())