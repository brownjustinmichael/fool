from django.db import models
from django.core.urlresolvers import reverse

class Card (models.Model):
    # This field is required.
    name = models.CharField (max_length = 20)
    strength = models.IntegerField ()
    
    def __str__ (self):
        return u"%s" % self.name
