import collections

from django.db import models
from cards.models import DEFENSE_BONUS, PLAYER_STATS, NPCTemplate, Score, CARD_IN_DECK

playerStats = collections.OrderedDict ()
for stat in PLAYER_STATS:
    playerStats [stat [0]] = models.IntegerField (default = 0)

class AbstractNPC (models.Model):
    """An NPC class is a database entry for a non-playable character. These can be people or objects."""
    # This is the event called when the NPC card is the top card in the event stack
    name = models.CharField (max_length = 30)
    slug = models.SlugField (unique=True, max_length=255, null = True, blank = True)
    genericEvent = models.ForeignKey ("events.Event", blank = True, null = True, related_name = "_unused_4")
    deck = models.ForeignKey ("cards.deck", blank = True, null = True)
    
    class Meta:
        abstract = True
        
    def __str__ (self):
        return self.name
        
    def getInstance (self, player):
        """
        If there's a deckStatus object associated with this deck and player, return it; otherwise, make one and return that
        """
        npcInstance = self.npcinstance_set.filter (player = player).first ()
        if npcInstance is None:
            npcInstance = NPCInstance (player = player, npc = self)
        return npcInstance
        
    def drawCard (self, player, **kwargs):
        return self.getInstance (player).drawCard (**kwargs)
        
playerStats.update ({"__module__": __name__})
NPC = type ('NPC', (AbstractNPC,), playerStats)

def createNPCTemplate (instance, created, raw, **kwargs):
    """
    This function should be run after each NPC instance is saved, and it will create an NPCTemplate associated with the NPC if one does not already exist.
    """
    if instance.npctemplate_set.count () == 0:
        template = NPCTemplate (npc = instance, name = str (instance))
        template.save ()

models.signals.post_save.connect (createNPCTemplate, sender = NPC, dispatch_uid = 'createNPCTemplate')

class NPCInstance (models.Model):
    player = models.ForeignKey ("accounts.Player")
    npc = models.ForeignKey (NPC)
    
    # TODO Treat life as modifier, and add modifiers for other stats
    @property
    def life (self):
        if self.deckStatus is None:
            return 0
        return self.deckStatus.getNumCards (CARD_IN_DECK)
    
    @property
    def deckStatus (self):
        if self.npc.deck is None:
            return None
        return self.npc.deck.getStatus (player = self.player)

    def discard (self, number):
        # TODO This should eventually deal with decks
        self.deckStatus.discard (number)
        
    def defend (self, scores):
        return Score (DEFENSE_BONUS [scores [0].stat], getattr (self.npc, DEFENSE_BONUS [scores [0].stat]))
        
    def drawCard (self, **kwargs):
        if self.npc is not None and self.npc.deck is not None:
            return self.npc.deck.getStatus (self.player).drawCard (**kwargs)
        
    def playCard (self, card = None):
        if card is None:
            card = self.drawCard ()
        if not isinstance (card, CardStatus):
            cardstatus = card.getStatus (self)
        else:
            cardstatus = card
        if cardstatus.card.template.stat is not None:
            return cardstatus.play () + getattr (self.npc, cardstatus.card.template.stat)
        return cardstatus.play ()
    
    class Meta:
        unique_together = ("player", "npc")
    
class NPCLink (models.Model):
    npc = models.ForeignKey (NPC)
    event = models.ForeignKey ("events.Event")
    card = models.ForeignKey ("cards.BaseCard", blank = True, null = True)
    
