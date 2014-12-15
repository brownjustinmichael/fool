from django.db import models

from results.models import Result
from cards.models import CardTemplate
from npcs.models import NPC, NPCInstance

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
        
    def trigger_event (self, player, cardStatus, template, strength, npc = None, played = True):
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
            player.addEvent (cardStatus = cardStatus, event = trigger.first ().event)
            #Return the trigger or None
            return trigger.first ()
            
    def trigger_result (self, player, template, strength, npc = None, played = True):
        # Filter the triggers by type and strength such that the first trigger satisfies the criteria best
        if self.npc is not None:
            trigger = self.resultcondition_set.filter (card = template).filter (success_threshold__gte = self.npc.life + npc.life).order_by ('success_threshold')
        else:
            trigger = self.resultcondition_set.filter (card = template).filter (success_threshold__lte = strength).order_by ('-success_threshold')
            
        # If there is a remaining trigger, enact the result
        if trigger.first () is not None:
            trigger.first ().success_result.enact (player)
            if (trigger.first ().success):
                lastEvent = player.activeevent_set.last ()
                if lastEvent is not None:
                    lastEvent.delete ()
            player.save ()
            #Return the trigger or None
            return trigger.first ()
    
    def resolve (self, player, location, card = None):
        """
        Resolve an event with or without a card to play. If the event can't resolve with current conditions, return None
        
        Note: this method calls the card.draw () method, which effectively moves the card to the discard pile and puts any special abilities of that card into effect.
        """
        
        if card is None and not self.auto:
            return None
        
        if card is not None:
            # If there is a card, play it
            stat, value = player.playCard (card)
            if self.npc is not None:
                try:
                    npc = self.npc.npcinstance_set.filter (player = player).first ()
                except Exception as e:
                    npc = NPCInstance (player = player, npc = self.npc)
                player.attack (npc, [(stat, value)])
            
            # Get the possible result conditionals (0 or 1)
            resultcondition = self.trigger_result (player, card.template, value, npc, True)
            if resultcondition is not None:
                card.resolve (player)
                print (resultcondition.content)
                return resultcondition
                
            # Try to trigger an event with the card
            eventtrigger = self.trigger_event (player, card.getStatus (player), card.template, value, npc, True)
            if eventtrigger is not None:
                card.resolve (player)
                print (eventtrigger.content)
                return eventtrigger
                
            card.resolve (player)
                
        # If nothing else works, use the generic result
        self.generic_result.enact (player)
        print (self.generic_content)
        if (self.generic_resolved):
            lastEvent = player.activeevent_set.last ()
            if lastEvent is not None:
                lastEvent.delete ()
            player.save ()
        
        return None
        
class EventTrigger (models.Model):
    """docstring for EventTrigger """
    originalEvent = models.ForeignKey (Event, null = True)
    template = models.ForeignKey (CardTemplate)
    event = models.ForeignKey (Event, null = True, related_name = "_unused_2")
    threshold = models.IntegerField (default = 0)
    onlyWhenNotPlayed = models.BooleanField (default = False)
    content = models.TextField (default = "")

class ResultCondition (models.Model):
    """
    This is the table that links results to events. It contains the ability to check whether the value of a card was sufficient for a successful result.
    In the future, capacities such as overkill and critical failures should be added here.
    """
    event = models.ForeignKey (Event)
    success = models.BooleanField (default = False)
    success_result = models.ForeignKey (Result, related_name = "_unused_1")
    card = models.ForeignKey (CardTemplate)
    content = models.TextField (default = "")

    success_threshold = models.IntegerField (default = 0)

    class Meta:
      unique_together = ('event', 'card',)

    def checkSuccess (self, cardValue):
        """
        The main method of the class, determines whether a cardValue is sufficient for success.
        """
        if cardValue >= self.success_threshold:
            return self.success_result
        else:
            return self.fail_result
            