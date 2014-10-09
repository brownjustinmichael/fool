from django.db import models
from django.core.urlresolvers import reverse

from cards.models import Deck, CardTemplate
from events.models import Event

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
        
    def trigger_event (self, player, cardstatus):
        stat, strength = cardstatus.play ()
        trigger = self.eventtrigger_set.filter (template = cardstatus.card.template).filter (threshold__lte = strength).order_by ('-threshold').first ()
        if trigger is not None:
            player.active_event = trigger.event
            player.active_location = self
            player.save ()
            return trigger.event

class EventTrigger (models.Model):
    """docstring for EventTrigger """
    location = models.ForeignKey (Location)
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey (Event)
    threshold = models.IntegerField (default = 0)

# Create your models here.
