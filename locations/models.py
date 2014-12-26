from django.db import models
from django.core.urlresolvers import reverse

from cards.models import Deck, CardTemplate
from events.models import Event
from accounts.models import ActiveEvent

class Location (models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    canshuffle = models.BooleanField (default = False)
    deck = models.OneToOneField (Deck, null = True, blank = True)
 
    class Meta:
        ordering = ['-created']
 
    def __str__ (self):
        return u'%s' % self.title
 
    def get_absolute_url(self):
        return reverse('locations.views.location', args=[self.slug])
        
    def trigger_event (self, player, cardStatus, location, played = True):
        stat, strength = cardStatus.play (played = played)
        # Filter the triggers by type and strength such that the first trigger satisfies the criteria
        print ("Triggering event now", player.activeevent_set.all ())
        trigger = self.locationtrigger_set.filter (template = cardStatus.card.template).filter (threshold__lte = strength).order_by ('-threshold')
        
        print ("Triggers", trigger.all (), self.locationtrigger_set.all () [0].template, cardStatus.card.template)
        
        # Filter out triggers based on whether a user played it
        if played:
            trigger = trigger.filter (onlyWhenNotPlayed = False)
            
        # If there is a remaining trigger, add the event to the stack
        if trigger.first () is not None:
            player.addEvent (cardStatus = cardStatus, event = trigger.first ().event, location = location)
            #Return the trigger or None
            return trigger.first ()

class GlobalEventTrigger (models.Model):
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey (Event)
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)

class LocationTrigger (models.Model):
    """docstring for EventTrigger """
    location = models.ForeignKey (Location)
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey (Event)
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)
    content = models.TextField (default = "")

# Create your models here.
