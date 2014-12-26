from django.db import models

from results.models import Result
from cards.models import CardTemplate
from npcs.models import NPC, NPCInstance

# class EffectEventLink (models.Model):
#     template = models.ForeignKey (CardTemplate)
#     effect = models.ForeignKey (Effect)

class Event (models.Model):
    """
    This class is designed to contain an event and handle its resolution by choosing the appropriate contained result object 
    """
    #Basic information about the event
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    
    description = models.CharField(max_length=255)
    content = models.TextField()
    
    npc = models.ForeignKey (NPC, null = True, blank = True)
    
    # Useful meta data about the class
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    # The generic result is what happens when the event is forced to resolve, but no 
    generic_result = models.ForeignKey (Result)
    generic_resolved = models.BooleanField (default = False)
    generic_content = models.TextField (default = "")
    auto = models.BooleanField (default = False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return u'%s' % self.title
        
    def trigger_event (self, player, cardStatus, template, strength, location, npc = None, played = True):
        # Filter the triggers by type and strength such that the first trigger satisfies the criteria
        # TODO cardStatus could keep track of its play values if it was just played
        if npc is not None:
            trigger = self.eventtrigger_set.filter (template = template).filter (threshold__gte = self.npc.life + npc.life).order_by ('threshold')
        else:
            trigger = self.eventtrigger_set.filter (template = template).filter (threshold__lte = strength).order_by ('-threshold')
            
        # Filter out triggers based on whether a user played it
        if played:
            trigger = trigger.filter (onlyWhenNotPlayed = False)
            
        # If there is a remaining trigger, add the event to the stack
        if trigger.first () is not None:
            player.addEvent (cardStatus = cardStatus, event = trigger.first ().event, location = location)
            #Return the trigger or None
            return trigger.first ()
    
    def resolve (self, player, location, cardStatus = None):
        """Resolve an event with or without a card to play. If the event can't resolve with current conditions, return None
        
        Note: this method calls the card.draw () method, which effectively moves the card to the discard pile and puts any special abilities of that card into effect."""
        
        if cardStatus is None and not self.auto:
            return (None, False)
        
        if cardStatus is not None:
            # If there is a card, play it
            stat, value = player.playCard (cardStatus)
            if self.npc is not None:
                try:
                    npc = self.npc.npcinstance_set.filter (player = player).first ()
                except Exception as e:
                    npc = NPCInstance (player = player, npc = self.npc)
                player.attack (npc, [(stat, value)])
                
            # Try to trigger an event with the card
            eventtrigger = self.trigger_event (player, cardStatus, cardStatus.card.template, value, location, npc, True)
            if eventtrigger is not None:
                cardStatus.resolve ()
                return (eventtrigger, False)
                
            print ("Resolving...")
            cardStatus.resolve ()
                
        # If nothing else works, use the generic result
        self.generic_result.enact (player)
        return (self.generic_result, True)
        
class EventTrigger (models.Model):
    """
    The EventTrigger links an event to possible sub-events
    
    """
    
    # The original event from which this EventTrigger can be triggered
    originalEvent = models.ForeignKey (Event, null = True)
    
    # The CardTemplate that this EventTrigger can be triggered by
    template = models.ForeignKey (CardTemplate)
    
    # The threshold that this card must beat in order to activate successfully. This is either the quantity that the card score must beat or the maximum remaining life of the associated NPC to be successful
    threshold = models.IntegerField (default = 0)
    
    # The event triggered by this EventTrigger, if this is None, the EventTrigger happens, but returns to the previous event
    event = models.ForeignKey (Event, null = True, related_name = "_unused_2")
    
    # Particular cards, e.g. item cards, have different effects when found than when played. This boolean is true for an event triggered ONLY when the card is put into play directly from a non-player deck
    onlyWhenNotPlayed = models.BooleanField (default = False)
    
    # The content of an EventTrigger is the text displayed as the 'result' text in the log
    content = models.TextField (default = "")
    
    # If this trigger resolves the parent event, this boolean is True
    resolved = models.BooleanField (default = True)
    
    def __str__ (self):
        return "%s (%s %d) -> %s" % (str (self.originalEvent), str (self.template), self.threshold, str (self.event))
