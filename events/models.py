from django.db import models
from django.db.models import Q
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
    tolog = models.BooleanField (default = True)
    
    #Basic information about the event
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    
    description = models.CharField(max_length=255,default = "",blank=True)
    content = models.TextField(default = "",blank=True)
    
    npc = models.ForeignKey (NPC, null = True, blank = True)
    
    # Useful meta data about the class
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    # The generic result is what happens when the event is forced to resolve, but no triggers have been matched
    generic_result = models.ForeignKey ("events.EventTrigger", default = None, null = True, related_name = "_unused_event_result", blank = True)
    auto = models.BooleanField (default = False)
    
    locationDeck = models.ForeignKey (Deck, null = True, blank = True, related_name = "event")
    deck = models.ForeignKey (Deck, null = True, blank = True, related_name = "_unused_event_location")
    
    blocking = models.BooleanField (default = False)
    canshuffle = models.BooleanField (default = False)
    

    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return '%s' % self.title
        
    @property
    def contentFlags (self):
        return list (set ([tag for tag in re.findall (r"\{\{(.*?)\?", self.title + self.content)]))
        
    def trigger_event (self, player, cardStatus, played = True, scores = None, value = 0, local = True):
        # Filter the triggers by type and strength such that the first trigger satisfies the criteria
        # TODO cardStatus could keep track of its play values if it was just played
        # If there is a card, play it
        print ("triggering")
        
        trigger = self.eventtrigger_set.filter (Q (template = cardStatus.card.template) | Q (template__isnull = True))
        
        print ("Found triggers", trigger.all ())
        
        return self.narrow_trigger (player, cardStatus, trigger, played, scores = scores, value = value, local = local)
        
    def narrow_trigger (self, player, cardStatus, triggers, played = True, scores = None, value = 0, local = True):
        print ("Generating NPC")
        npc = self.generateNPCInstance (player)
        if len (triggers) == 0:
            return None
        
        npctriggers = []
        valuetriggers = []
        for trigger in triggers:
            if played:
                if trigger.onlyWhenNotPlayed:
                    continue
            if not local:
                if trigger.localOnly:
                    continue
            if trigger.npcthreshold:
                npctriggers.append (trigger)
            else:
                valuetriggers.append (trigger)
                
        valuetriggers.reverse ()
                
        triggers = npctriggers + valuetriggers
        
        print ("LLAMA THINKING ABOUT TRIGGER:", triggers)
            
        if played:
            if npc is not None and scores is not None:
                player.attack (npc, scores)
        
        npclife = None
        if npc is not None:
            npclife = npc.life
            
        last = None
        for tr in triggers:
            if tr.checkTrigger (player, value, npclife):
                last = tr
                print ("Success with ", tr)
                break
            print ("I FAILLLLLLLED")
        return last
        
        
    def generateNPCInstance (self, player):
        if self.npc is not None:
            npc = self.npc.npcinstance_set.filter (player = player).first ()
            if npc is None:
                npc = NPCInstance (player = player, npc = self.npc)
                npc.save ()
            return npc
    
    def resolve (self, player, cardStatus = None, played = True, triggers = None, local = True):
        """Resolve an event with or without a card to play. If the event can't resolve with current conditions, return None
        
        Note: this method calls the card.draw () method, which effectively moves the card to the discard pile and puts any special abilities of that card into effect."""
        print ("LLAMA RESOLUTION")
        if cardStatus is None and not self.auto:
            return None
        
        scores = []
        value = 0
        if cardStatus is not None:
            scores = player.playCard (cardStatus)
            print ("Card played")
            if len (scores) > 0:
                value = scores [0].value
            else:
                value = cardStatus.card.modifier
        
        if triggers is not None:
            print ("NARROW TRIGGER TIME")
            trigger = self.narrow_trigger (player, cardStatus = cardStatus, triggers = triggers, played = played, scores = scores, value = value, local = local)
            if trigger is not None:
                return trigger
        
        if cardStatus is not None:
            print ("EVENT TRIGGER TIME")
            # Try to trigger an event with the card
            eventtrigger = self.trigger_event (player, cardStatus, played = played, scores = scores, value = value, local = local)
            if eventtrigger is not None:
                return eventtrigger
                
            print ("Resolving...")
            cardStatus.resolve ()
                
        # If nothing else works, use the generic result
        if self.generic_result is not None and local:
            print ("IM BASIC",self, self.generic_result)
            return self.generic_result
        return None
        
    def drawCard (self, player):
        """
        Draw a card from the location deck. Check whether this card triggers any events.
        """
        if self.locationDeck is not None:
            print ("event draw")
            card = self.locationDeck.drawCard (player)
            card.play ()
            print (card)
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
    
        
class EventTrigger (models.Model):
    """
    The EventTrigger links an event to possible sub-events
    
    """
    
    class Meta:
        ordering = ['event', 'threshold', 'template']
    
    # The original event from which this EventTrigger can be triggered
    originalEvent = models.ForeignKey (Event, null = True, blank = True)
    
    # The CardTemplate that this EventTrigger can be triggered by
    template = models.ForeignKey (CardTemplate, null = True, blank = True)
    
    # The threshold that this card must beat in order to activate successfully. This is either the quantity that the card score must beat or the maximum remaining life of the associated NPC to be successful
    threshold = models.IntegerField (default = 0)
    npcthreshold = models.BooleanField (default = True)
    
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
    result = models.CharField (max_length = 8, choices = RESULTS, blank = True, null = True, default = None)
    
    # If this trigger resolves the parent event, this boolean is True
    @property
    def resolved (self):
        return self.result == RESOLVE
        
    @property
    def switch (self):
        return self.result == SWITCH
        
    def checkTrigger (self, player, value, npclife = None):
        print ("Checking", self, "with", self.npcthreshold, npclife, value)
        if self.npcthreshold:
            if npclife is not None:
                return CompositeFlag.fromString (self.conditions).state (player) and npclife <= self.threshold
        else:
            print ("Checking", self.conditions, CompositeFlag.fromString (self.conditions).state (player))
            return CompositeFlag.fromString (self.conditions).state (player) and value >= self.threshold
        return False
    
    @property
    def title (self):
        return self.originalEvent.title
    
    def __str__ (self):
        return "%s (%s %d) -> %s" % (str (self.originalEvent), str (self.template), self.threshold, str (self.event))

class EventEffect (models.Model):
    event = models.ForeignKey (Event)
    effect = models.ForeignKey ("cards.Effect")