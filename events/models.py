from django.db import models

from results.models import Result
from cards.models import CardTemplate
 
class Event (models.Model):
    """
    This class is designed to contain an event and handle its resolution by choosing the appropriate contained result object 
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    
    description = models.CharField(max_length=255)
    content = models.TextField()
    
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    generic_result = models.ForeignKey (Result)
    auto = models.BooleanField (default = False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return u'%s' % self.title
        
    def resolve (self, player, location, card = None):
        if card is not None:
            value = card.play ()
            resultconditions = self.resultcondition_set.filter (card = card.template).all ()
            if len (resultconditions) > 1:
                raise LookupError ("More than one match for card type %s" % card.template.name)
            elif len (resultconditions) == 1:
                result = resultconditions [0].checkSuccess (value)
            else:
                result = self.generic_result
        else:
            if not self.auto:
                return
            else:
                result = self.generic_result
        player.recordLog (event = self, result = result, location = location)
        print ("Resolving...")
        return result.enact (player)
        
class ResultCondition (models.Model):
    event = models.ForeignKey (Event)
    success_result = models.ForeignKey (Result, related_name = "_unused_1")
    fail_result = models.ForeignKey (Result, related_name = "_unused_2")
    card = models.ForeignKey (CardTemplate)

    success_threshold = models.IntegerField (default = 0)

    class Meta:
      unique_together = ('event', 'card',)

    def checkSuccess (self, cardValue):
        if cardValue >= self.success_threshold:
            return self.success_result
        else:
            return self.fail_result
            