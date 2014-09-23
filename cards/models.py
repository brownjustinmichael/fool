from django.db import models
from accounts.models import UserProfile, CARD_STATUSES, CARD_IN_STASH
from django.core.urlresolvers import reverse

class Card (models.Model):
    # This field is required.
    name = models.CharField (max_length = 20)
    strength = models.IntegerField ()
    
    def __str__ (self):
        return u"%s" % self.name
        
class CardAttributes (models.Model):
    player = models.ForeignKey (UserProfile)
    card = models.ForeignKey (Card)
    modifier = models.IntegerField ()
    status = models.CharField (max_length = 6, choices = CARD_STATUSES, default = CARD_IN_STASH)
    
    def __str__ (self):
        return u"%s's %s" % (self.player.user, self.card)
        
    def get_absolute_url (self):
        return reverse ('cards.views.card', args=[self.id])
        