from django.db import models

from results.models import Result
from cards.models import CardTemplate
 
class Event (models.Model):
    """
    This class is designed to contain an event and handle its resolution by choosing the appropriate contained result object 
    """
    #Basic information about the event
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    
    description = models.CharField(max_length=255)
    content = models.TextField()
    
    # Useful meta data about the class
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    # The generic result is what happens when the event is forced to resolve, but no 
    generic_result = models.ForeignKey (Result)
    auto = models.BooleanField (default = False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return u'%s' % self.title
        
    def resolve (self, player, location, card = None):
        """
        Resolve an event with or without a card to play. If the event can't resolve with current conditions, return None
        
        Note: this method calls the card.draw () method, which effectively moves the card to the discard pile and puts any special abilities of that card into effect.
        """
        if card is not None:
            # If there is a card, play it
            value = card.play ()
            
            # Get the possible result conditionals (0 or 1)
            resultconditions = self.resultcondition_set.filter (card = card.template).order_by (success_threshold).all ()
            
            #If there is one, check it
            if len (resultconditions) == 1:
                result = resultconditions [0].checkSuccess (value)
                
            # If not, use the generic result
            else:
                result = self.generic_result
        else:
            #If the card isn't set to auto and there's no played card, it can't resolve
            if not self.auto:
                return
                
            # If it is, use the generic result
            else:
                result = self.generic_result
                
        # Record the event/result pair in the log
        player.recordLog (event = self, result = result, location = location)
        
        # Enact the result
        return result.enact (player)
        
class ResultCondition (models.Model):
    """
    This is the table that links results to events. It contains the ability to check whether the value of a card was sufficient for a successful result.
    In the future, capacities such as overkill and critical failures should be added here.
    """
    event = models.ForeignKey (Event)
    success_result = models.ForeignKey (Result, related_name = "_unused_1")
    fail_result = models.ForeignKey (Result, related_name = "_unused_2")
    card = models.ForeignKey (CardTemplate)

    success_threshold = models.IntegerField (default = 0)

    class Meta:
      unique_together = ('event', 'card',)

    def checkSuccess (self, cardValue):
        """
        The main method of the class, determines whether a cardValue is sufficient for success.
        """
        if cardValue >= self.success_threshold:
            return (True, self.success_result)
        else:
            return (False, self.fail_result)
            