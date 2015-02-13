from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from cards.models import Deck, CardTemplate, NPCCard
from accounts.models import Flag

# TODO Since you can complete tasks outside of the active location, logs can be stored outside the location they happen

class Location (models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField(default = "", blank = True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    canshuffle = models.BooleanField (default = False)
    deck = models.OneToOneField (Deck, blank = True)
 
    class Meta:
        ordering = ['-created']
 
    def __str__ (self):
        return u'%s' % self.title
        
    def save (self, *args, **kwargs):
        print (args, kwargs)
        try:
            print ("HERE")
            if self.deck is None:
                newdeck = Deck ()
                newdeck.save ()
                self.deck = newdeck
        except ObjectDoesNotExist:
            print ("THERE")
            newdeck = Deck ()
            newdeck.save ()
            self.deck = newdeck
        return super (Location, self).save (*args, **kwargs)
 
    def get_absolute_url(self):
        return reverse('locations.views.location', args=[self.slug])
        
    def trigger_event (self, player, cardStatus, played = True):
        scores = cardStatus.play (played = played)
        if len (scores) > 0:
            stat, strength = scores [0]
        else:
            strength = 0
        # Filter the triggers by type and strength such that the first trigger satisfies the criteria
        trigger = self.locationtrigger_set.filter (template = cardStatus.card.template).filter (threshold__lte = strength).order_by ('-threshold')
                
        # Filter out triggers based on whether a user played it
        if played:
            trigger = trigger.filter (onlyWhenNotPlayed = False)
            
        # If there is a remaining trigger, add the event to the stack
        if trigger.first () is not None:
            player.addEvent (cardStatus = cardStatus, event = trigger.first ().event, location = self)
            #Return the trigger or None
            return trigger.first ()
            
    def drawCard (self, player):
        """
        Draw a card from the location deck. Check whether this card triggers any events.
        """
        print (self.deck)
        if self.deck is not None:
            if player.activeevent_set.count () > 0:
                raise RuntimeError ("You can't draw from the location deck if there are still active events.")
            else:
                self.trigger_event (player, self.deck.drawCard (player), played = False)
                
    def playCard (self, player, cardStatus):
        """
        Draw a card from the location deck. Check whether this card triggers any events.
        """
        if player.activeevent_set.count () > 0:
            raise RuntimeError ("You can't play from the location deck if there are still active events.")
        else:
            self.trigger_event (player, cardStatus, played = False)
    
    @property
    def npcLinks (self):
        return self.npclink_set.all ()
    
    
class GlobalEventTrigger (models.Model):
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey ("events.Event")
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)

class LocationTrigger (models.Model):
    """docstring for EventTrigger """
    location = models.ForeignKey (Location)
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey ("events.Event")
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)
    content = models.TextField (default = "", blank = True)

# Create your models here.
