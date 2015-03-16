from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from cards.models import Deck, CardTemplate, NPCCard
from accounts.models import Flag
from events.models import Event

# TODO Since you can complete tasks outside of the active location, logs can be stored outside the location they happen

class Location (Event):
    tolog = False
    
    def save (self, *args, **kwargs):
        print (args, kwargs)
        try:
            if self.deck is None:
                newdeck = Deck ()
                newdeck.save ()
                self.deck = newdeck
        except ObjectDoesNotExist:
            newdeck = Deck ()
            newdeck.save ()
            self.deck = newdeck
        return super (Location, self).save (*args, **kwargs)
 
    def get_absolute_url(self):
        return reverse('locations.views.location', args=[self.slug])
    
class GlobalEventTrigger (models.Model):
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey ("events.Event")
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)

# Create your models here.
