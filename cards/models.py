from django.db import models

FORCE = "force"
DASH = "dash"
RESIST = "resist"
CHARM = "charm"
WISDOM = "wisdom"
POWER = "power"
MONEY = "money"
PLAYER_STATS = ((FORCE, "Force"), (DASH, "Dash"), (RESIST, "Resist"), (CHARM, "Charm"), (WISDOM, "Wisdom"), (POWER, "Power"), (MONEY, "Money"))

class CardTemplate (models.Model):
    """
    This class is designed to contain the more complex workings of the card class, which will include leveling mechanisms, socketing capacity, and subclasses for strange cards like Tarot and Item
    """
    name = models.CharField (max_length = 20)
    stat = models.CharField (max_length = 8, choices = PLAYER_STATS, blank = True)
    
    def __str__ (self):
        return u"%s Template" % self.name
