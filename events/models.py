from django.db import models
import re

from cards.models import CardTemplate, Deck
from npcs.models import NPC, NPCInstance
from accounts.models import CompositeFlag

# class EffectEventLink (models.Model):
#     template = models.ForeignKey (CardTemplate)
#     effect = models.ForeignKey (Effect)

RESOLVE = "resolve"
SWITCH = "switch"
RESULTS = ((RESOLVE, "Resolve"), (SWITCH, "Switch"))

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
    
    # The generic result is what happens when the event is forced to resolve, but no triggers have been matched
    generic_result = models.ForeignKey ("events.EventTrigger", default = None, null = True, related_name = "_unused_event_result", blank = True)
    auto = models.BooleanField (default = False)
    
    deck = models.ForeignKey (Deck, null = True, blank = True)
    
    blocking = models.BooleanField (default = False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return u'%s' % self.title
        
    @property
    def contentFlags (self):
        return list (set ([tag for tag in re.findall (r"\{\{(.*?)\?", self.title + self.content)]))
        
    def trigger_event (self, player, cardStatus, played = True):
        # Filter the triggers by type and strength such that the first trigger satisfies the criteria
        # TODO cardStatus could keep track of its play values if it was just played
        # If there is a card, play it
        scores = player.playCard (cardStatus)
        npc = self.generateNPCInstance (player)
            
        # Filter out triggers based on whether a user played it
        if played:
            trigger = self.eventtrigger_set.filter (template = cardStatus.card.template).order_by ('threshold')
            if npc is not None:
                player.attack (npc, scores)
                value = npc.life
            else:
                if len (scores) > 0:
                    value = -scores [0].value
                else:
                    value = 0
            trigger = trigger.filter (onlyWhenNotPlayed = False)
        else:
            if npc is not None:
                pass
                # npc.attack (player, [(template, strength)])
            trigger = self.eventtrigger_set.filter (template = cardStatus.card.template).order_by ('threshold')
            if len (scores) > 0:
                value = -scores [0].value
            else:
                value = 0
            
        # If there is a remaining trigger, add the event to the stack
        last = None
        for tr in trigger.all ():
            if tr.checkTrigger (player, value):
                last = tr
                break
        return last
        
    def generateNPCInstance (self, player):
        if self.npc is not None:
            npc = self.npc.npcinstance_set.filter (player = player).first ()
            if npc is None:
                npc = NPCInstance (player = player, npc = self.npc)
                npc.save ()
            return npc
    
    def resolve (self, player, cardStatus = None, played = True):
        """Resolve an event with or without a card to play. If the event can't resolve with current conditions, return None
        
        Note: this method calls the card.draw () method, which effectively moves the card to the discard pile and puts any special abilities of that card into effect."""
        
        if cardStatus is None and not self.auto:
            return None
        
        if cardStatus is not None:
                
            # Try to trigger an event with the card
            eventtrigger = self.trigger_event (player, cardStatus, played)
            if eventtrigger is not None:
                return eventtrigger
                
            print ("Resolving...")
            cardStatus.resolve ()
                
        # If nothing else works, use the generic result
        if self.generic_result is not None:
            return self.generic_result
        return None
        
class EventTrigger (models.Model):
    """
    The EventTrigger links an event to possible sub-events
    
    """
    
    class Meta:
        ordering = ['event', 'template', 'threshold']
    
    # The original event from which this EventTrigger can be triggered
    originalEvent = models.ForeignKey (Event, null = True, blank = True)
    
    # The CardTemplate that this EventTrigger can be triggered by
    template = models.ForeignKey (CardTemplate)
    
    # The threshold that this card must beat in order to activate successfully. This is either the quantity that the card score must beat or the maximum remaining life of the associated NPC to be successful
    threshold = models.IntegerField (default = 0)
    
    helper = models.CharField (max_length = 256, default = "", blank = True)
    
    conditions = models.CharField (max_length = 256, default = "", blank = True)
    
    # The event triggered by this EventTrigger, if this is None, the EventTrigger happens, but returns to the previous event
    event = models.ForeignKey (Event, null = True, blank = True, related_name = "_unused_2")
    
    # Particular cards, e.g. item cards, have different effects when found than when played. This boolean is true for an event triggered ONLY when the card is put into play directly from a non-player deck
    onlyWhenNotPlayed = models.BooleanField (default = False)
    localOnly = models.BooleanField (default = False)
    
    # The content of an EventTrigger is the text displayed as the 'result' text in the log
    content = models.TextField (default = "", blank = True)

    # 
    result = models.CharField (max_length = 8, choices = RESULTS, blank = True, null = True, default = RESOLVE)
    
    def getResolved (self):
        return self.result == RESOLVE
    
    # If this trigger resolves the parent event, this boolean is True
    resolved = property (getResolved)
    
    def getSwitch (self):
        return self.result == SWITCH
        
    switch = property (getSwitch)
    
    def checkTrigger (self, player, value):
        print ("CHECKING")
        print (CompositeFlag.fromString (self.conditions).state (player))
        print (value, self.threshold)
        return CompositeFlag.fromString (self.conditions).state (player) and value <= self.threshold
    
    @property
    def title (self):
        return self.originalEvent.title
    
    def __str__ (self):
        return "%s (%s %d) -> %s" % (str (self.originalEvent), str (self.template), self.threshold, str (self.event))

class LocationTrigger (EventTrigger):
    """docstring for EventTrigger """
    location = models.ForeignKey ("locations.Location")

class EventEffect (models.Model):
    event = models.ForeignKey (Event)
    effect = models.ForeignKey ("cards.Effect")