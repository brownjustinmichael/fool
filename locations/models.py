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
        scores = player.playCard (cardStatus)
            
        # Filter out triggers based on whether a user played it
        if played:
            trigger = self.locationtrigger_set.filter (template = cardStatus.card.template).order_by ('threshold')
            if len (scores) > 0:
                value = -scores [0].value
            else:
                value = -cardStatus.card.modifier
            trigger = trigger.filter (onlyWhenNotPlayed = False)
        else:
            trigger = self.locationtrigger_set.filter (template = cardStatus.card.template).order_by ('threshold')
            if len (scores) > 0:
                value = -scores [0].value
            else:
                value = -cardStatus.card.modifier
        
        # If there is a remaining trigger, add the event to the stack
        last = None
        for tr in trigger.all ():
            if tr.checkTrigger (player, value):
                last = tr
                break
                
        return last
            
    def drawCard (self, player):
        """
        Draw a card from the location deck. Check whether this card triggers any events.
        """
        if self.deck is not None:
            if player.activeevent_set.count () > 0:
                raise RuntimeError ("You can't draw from the location deck if there are still active events.")
            else:
                card = self.deck.drawCard (player)
                card.play ()
                return card
                
    def playCard (self, player, cardStatus):
        """
        Draw a card from the location deck. Check whether this card triggers any events.
        """
        if player.activeevent_set.count () > 0:
            raise RuntimeError ("You can't play from the location deck if there are still active events.")
        else:
            cardStatus.play ()
            player.resolve (self, cardStatus, played = False)
    
    @property
    def npcLinks (self):
        return self.npclink_set.all ()
    
    
class GlobalEventTrigger (models.Model):
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey ("events.Event")
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)

# Create your models here.
