from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

from polymorphic import PolymorphicModel
from django.core.urlresolvers import reverse
from cards.models import PLAYER_STATS, EXTRA_STATS, FORCE, DASH, RESIST, CHARM, WISDOM, POWER, MONEY

class Result (PolymorphicModel):
    """
    This class is designed to be a super class to any result to an event card
    """
    name = models.CharField (max_length = 20)
    message = models.TextField ()
        
    def __str__ (self):
        return u"%s" % self.name
        
    def enact (self, userprofile):
        """
        This is the main function that the result class wraps. Given that a particular result has been decided, this enacts it. It should be overridden for each type of possible result
        """
        userprofile.active_event = None
        userprofile.active_location = None
        userprofile.save ()
        return self.message
        
class StatResult (Result):
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS + EXTRA_STATS, null = True, default = None)

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
    new_event = models.ForeignKey ("events.Event", related_name = "_unused_3")
        
    def __str__ (self):
        return u"%s -> %s" % (self.name, str (self.new_event))
        
    def enact (self, userprofile):
        print ("Enacting")
        print (self.new_event)
        userprofile.active_event = self.new_event
        userprofile.save ()
        return self.message
        

