import collections

from django.db import models
from cards.models import DEFENSE_BONUS, PLAYER_STATS

playerStats = collections.OrderedDict ()
for stat in PLAYER_STATS:
    playerStats [stat [0]] = models.IntegerField (default = 0)

class AbstractNPC (models.Model):
    """An NPC class is a database entry for a non-playable character. These can be people or objects."""
    # This is the event called when the NPC card is the top card in the event stack
    name = models.CharField (max_length = 30)
    genericEvent = models.ForeignKey ("events.Event", related_name = "_unused_4")
    
    life = models.IntegerField ()
    
    class Meta:
        abstract = True
        
    def __str__ (self):
        return self.name
        

playerStats.update ({"__module__": __name__})
NPC = type ('NPC', (AbstractNPC,), playerStats)

class NPCInstance (models.Model):
    player = models.ForeignKey ("accounts.Player")
    npc = models.ForeignKey (NPC)
    
    # TODO Treat life as modifier, and add modifiers for other stats
    life = models.IntegerField (default = 0)
    
    def discard (self, number):
        # TODO This should eventually deal with decks
        self.life -= number
        self.save ()
        
    def defend (self, scores):
        return DEFENSE_BONUS [scores [0] [0]], getattr (self.npc, DEFENSE_BONUS [scores [0] [0]])
    
    class Meta:
        unique_together = ("player", "npc")
    
    