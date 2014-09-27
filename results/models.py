from django.db import models
from polymorphic import PolymorphicModel
from accounts.models import Player, CARD_STATUSES, CARD_IN_STASH
from django.core.urlresolvers import reverse
from events.models import Event
from cards.models import CardTemplate, PLAYER_STATS, FORCE, DASH, RESIST, CHARM, WISDOM, POWER, MONEY
from locations.models import Location

from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

class Result (PolymorphicModel):
    # This field is required.
    name = models.CharField (max_length = 20)
    message = models.TextField ()
        
    def __str__ (self):
        return u"%s" % self.name
        
    def enact (self, userprofile):
        userprofile.active_event = None
        userprofile.active_location = None
        print ("Super")
        return self.message
        
        
class StatResult (Result):
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS, null = True, default = None)

    modifier = models.IntegerField (default = 0)
    
    def enact (self, userprofile):
        userprofile.active_event = None
        userprofile.active_location = None
        if self.stat == FORCE:
            userprofile.force += self.modifier
        elif self.stat == DASH:
            userprofile.dash += self.modifier
        elif self.stat == RESIST:
            userprofile.resist += self.modifier
        elif self.stat == CHARM:
            userprofile.charm += self.modifier
        elif self.stat == WISDOM:
            userprofile.wisdom += self.modifier
        elif self.stat == POWER:
            userprofile.power += self.modifier
        elif self.stat == MONEY:
            userprofile.money += self.modifier
        return super (StatResult, self).enact (userprofile)

class EnemyResult (Result):
    # This field is required.
    enemy_name = models.CharField (max_length = 20)
        
    def __str__ (self):
        return u"%s, %s" % (self.name, self.enemy_name)
        
    def enact (self, userprofile):
        return super (EnemyResult, self).enact (userprofile)
        
class NewEventResult (Result):
    # This field is required.
    new_event = models.ForeignKey (Event, related_name = "_unused_3")
        
    def __str__ (self):
        return u"%s, %s" % (self.name, str (self.new_event))
        
    def enact (self, userprofile):
        print ("Enacting")
        userprofile.active_event = self.new_event
        return self.message
        
class ResultCondition (models.Model):
    event = models.ForeignKey (Event)
    success_result = models.ForeignKey (Result, related_name = "_unused_1")
    fail_result = models.ForeignKey (Result, related_name = "_unused_2")
    card = models.ForeignKey (CardTemplate)

    success_threshold = models.IntegerField (default = 0)

    class Meta:
      unique_together = ('event', 'card',)

    def checkSuccess (self, card):
        if card.play () >= self.success_threshold:
            return self.success_result
        else:
            return self.fail_result
            

class Log (models.Model):
    title = models.CharField (max_length = 255)
    event = models.ForeignKey (Event)
    result = models.ForeignKey (Result)
    location = models.ForeignKey (Location)
    logged = models.DateTimeField (auto_now_add=True)
    
    user = models.ForeignKey (Player)
    