from django.db import models
from django.core.urlresolvers import reverse

from cards.models import Deck

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

# Create your models here.
