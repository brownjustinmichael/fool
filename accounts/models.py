import random
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from polymorphic import PolymorphicModel

import abc
import re
import ast

import collections

from polymorphic import PolymorphicModel

from cards.models import CardTemplate, CARD_STATUSES, CARD_IN_STASH, CARD_IN_DECK, CARD_IN_DISCARD, CARD_IN_HAND, CARD_IN_PLAY, Deck, Card, BaseCard, PLAYER_STATS, EXTRA_STATS, DEFENSE_BONUS, OFFENSE_BONUS, RESIST, FORCE

stats = collections.OrderedDict ()
for stat in PLAYER_STATS + EXTRA_STATS:
    stats [stat [0]] = models.IntegerField (default = 0)

class CardStatus (models.Model):
    """
    A CardStatus object is an instance of a Card object
    """
    card = models.ForeignKey (BaseCard)
    deck = models.ForeignKey ('DeckStatus')
    status = models.CharField (max_length = 7, choices = CARD_STATUSES, default = CARD_IN_STASH)
    position = models.IntegerField ()
    played = models.BooleanField (default = False)
    targetDeck = models.ForeignKey ('DeckStatus', blank = True, null = True, default = None, related_name = '_unused_1')
    
    class Meta:
        unique_together = (('deck', 'position', 'status'))
        ordering = ['status', 'position']
        verbose_name_plural = "Card statuses"
        
    def __str__ (self):
        return "%s in (%s)" % (self.card, self.deck)
        
    @property
    def player (self):
        return self.deck.player
        
    def save (self, *args, **kwargs):
        """
        Saves the object to the database
        """
        # self.deck = self.card.deck
        if self.position == None:
            self.position = self.deck.getCards (status = self.status).order_by ("position").last ().position + 1
        return super (CardStatus, self).save (*args, **kwargs)
        
    def draw (self, next_status = CARD_IN_HAND):
        assert (next_status is not None)
        card = self.card.draw (next_status = next_status)
        self.status = next_status
        lastCard = self.deck.getCards (status = next_status).order_by ("position").last ()
        if lastCard is not None:
            self.position = lastCard.position + 1
        else:
            self.position = 0
        self.save ()
        return self
        
    def play (self, next_status = CARD_IN_PLAY, played = True):
        value = self.card.play (next_status = next_status)
        self.targetDeck = self.deck
        self.status = next_status
        self.played = played
        lastCard = self.deck.getCards (status = next_status).order_by ("position").last ()
        if lastCard is not None:
            self.position = lastCard.position + 1
        self.save ()
        return value
        
    def resolve (self, next_status = CARD_IN_DISCARD):
        self.card.resolve (self.deck.player, self.targetDeck, next_status = next_status)
        if CardStatus.objects.filter (id = self.id).count () > 0:
            self.status = next_status
            lastCard = self.deck.getCards (status = next_status).order_by ("position").last ()
            if lastCard is not None:
                self.position = lastCard.position + 1
            else:
                self.position = 0
            self.save ()
        
    def discard (self, next_status = CARD_IN_DISCARD):
        self.card.discard (next_status = next_status)
        self.status = next_status
        lastCard = self.deck.getCards (status = next_status).order_by ("position").last ()
        if lastCard is not None:
            self.position = lastCard.position + 1
        else:
            self.position = 0
        self.save ()
        
    def recover (self, next_status = CARD_IN_DECK):
        self.status = next_status
        lastCard = self.deck.getCards (status = next_status).order_by ("position").last ()
        if lastCard is not None:
            self.position = lastCard.position + 1
        else:
            self.position = 0
        self.save ()
        
    @property
    def helper (self):
        return self.player.active_event.getHelper (self.card.template)

class DeckStatus (models.Model):
    player = models.ForeignKey ('Player')
    deck = models.ForeignKey (Deck)
    location = models.ForeignKey ("locations.Location", blank = True, null = True)
    initialized = models.BooleanField (default = False)
    
    class Meta:
        unique_together = (('player', 'deck'))
        verbose_name_plural = "Deck statuses"
        
    def __str__ (self):
        return "%s viewed by %s" % (str (self.deck), str (self.player.user.username))
        
    def checkInitialize (self):
        if not self.initialized:
            self.initialize ()
        
    def initialize (self, default = CARD_IN_DECK):
        for cardstatus in self.cardstatus_set.all ():
            cardstatus.delete ()
        
        resetCards = []
        for card in self.deck.basecard_set.all ():
            if card.isActive ():
                resetCards.append (card)
        
        indices = list (range (len (resetCards)))
        random.shuffle (indices)
        itr = iter (indices)
        for card in resetCards:
            pos = next (itr)
            cardstatus = CardStatus (card = card, status = default, deck = self, position = pos)
            cardstatus.save ()
        
        self.initialized = True
        self.save ()
        
    def save (self, *args, **kwargs):
        try:
            self.location = self.deck.location
        except ObjectDoesNotExist:
            pass
        return super (DeckStatus, self).save (*args, **kwargs)
        
    def addNewCard (self, card, status = CARD_IN_HAND):
        card.deck = self.deck
        card.pk = None
        card.save ()
        if self.getCards (status = status).count () > 0:
            newpos = self.getCards (status = status).last ().position + 1
        else:
            newpos = 0
        cardstatus = CardStatus (card = card, deck = self, status = status, position = newpos)
        cardstatus.save ()
        
    def addCardStatus (self, card, status = CARD_IN_PLAY):
        if self.getCards (status = status).count () > 0:
            newpos = self.getCards (status = status).last ().position + 1
        else:
            newpos = 0
        cardstatus = CardStatus (card = card, deck = self, status = status, position = newpos)
        cardstatus.save ()
        return cardstatus
        
    def getNumCards (self, status = CARD_IN_DECK):
        """
        Return the number of cards currently in the deck
        """
        self.checkInitialize ()
        return self.cardstatus_set.filter (status = status).count ()
    
    def getCards (self, status = CARD_IN_HAND, **kwargs):
        """
        Return a list of the cards with current status
        """
        self.checkInitialize ()
        return self.cardstatus_set.filter (status = status, **kwargs)
        
    def drawCard (self, next_status = CARD_IN_HAND, force = False):
        """
        Return the CardStatus instance on top of the deck and set that card's status to next_status
        
        This method will raise an error if a card is attempted to be drawn from an empty deck or if there is an unresolved event
        
        next_status: The next status for the card drawn, by default CARD_IN_HAND
        force: If a card should be drawn regardless of whether there are events in play (e.g. an item card that lets the player draw), set force to True
        
        return: The CardStatus object drawn from the deck
        """
        self.checkInitialize ()
        # if not force and self.player.active_event is not None:
            # raise RuntimeError ("You can't draw from a deck if there's an unresolved event on the stack")
        
        cardstatus = self.cardstatus_set.filter (status = CARD_IN_DECK).order_by ('position').first ()
        if cardstatus is not None:
            return cardstatus.draw (next_status)
        raise ValueError ("You've run out of cards in this deck.")

    def playCard (self, card, next_status = CARD_IN_HAND):
        """
        Return the Card instance on top of the deck
        """
        self.checkInitialize ()
        return self.cardstatus_set.filter (card = card).first ().play (next_status)
        
    def discard (self, number, next_status = CARD_IN_DISCARD):
        """Discard the top number cards of the deck"""
        self.checkInitialize ()
        for i in range (number):
            cardstatus = self.cardstatus_set.filter (status = CARD_IN_DECK).order_by ('position').first ()
            if cardstatus is not None:
                return cardstatus.discard (next_status)
        raise ValueError ("You've run out of cards in this deck.")
        
    def reshuffle (self, **kwargs):
        """
        Move the cards in the discard pile to the deck
        """
        
        if self.player.active_event is not None:
            raise RuntimeError ("You can't shuffle a deck if there's an unresolved event on the stack")
        
        status = kwargs.pop ('status', None)

        resetCards = []
        if status is None:
            for cardstatus in self.cardstatus_set.filter (**kwargs).all ():
                cardstatus.delete ()
            for card in self.deck.basecard_set.all ():
                if card.isActive ():
                    resetCards.append (card)
        else:
            for cardstatus in self.cardstatus_set.filter (status = status, **kwargs).all ():
                resetCards.append (cardstatus.card)
                cardstatus.delete ()
        
        self.initialized = False
        self.delete ()

class AbstractPlayer (models.Model):
    """
    This object contains the critical information about the player needed to play the game. These include:
        user: A link to the user object associated with the player
        active_event: A link to the event object that's currently active
        active_location: A link to the location where the current event is active
        stats: A set of integer stat fields specified in USER_STATS
    """
    user = models.OneToOneField (User)
    deck = models.OneToOneField (Deck, null = True, blank = True, related_name = "player")
    
    class Meta:
        abstract = True
    
    def __str__ (self):
        return u"%s's Profile" % self.user.username
        
    @property
    def active_event (self):
        return self.activeevent_set.order_by ("stackOrder").last ()
        
    @property
    def active_events (self):
        return self.activeevent_set.order_by ("stackOrder").all ()
    
    def getActiveLocation (self):
        active = self.active_event
        if active is not None:
            return active.location
        else:
            return None
            
    active_location = property (getActiveLocation)
            
    def changeStat (self, stat, value):
        """Change the value of the player's stat by value"""
        setattr (self, stat, getattr (self, stat) + value)
        self.save () 
    
    def recordLog (self, event, result, location):
        Log (title = event.title, event = event, result = result, user = self, location = location).save ()
        
    def maxCardsInHand (self):
        return getattr (self, RESIST)
        
    handMax = property (maxCardsInHand)
        
    def maxCardsInDeck (self):
        return getattr (self, FORCE) * 4
        
    def draw (self, location):
        """
        Draw cards until your hand is full
        """
        print ("SHALL WE DRAW?")
        if (self.getCards (CARD_IN_HAND).count () >= self.maxCardsInHand ()):
            return
            raise RuntimeError ("You can't exceed the maximum number of cards in your hand")
        if self.active_location is not None:
            if location != self.active_location:
                raise RuntimeError ("You can only draw at the current active location")
        print (self.getCards (CARD_IN_HAND).count ())
        while self.getCards (CARD_IN_HAND).count () < self.maxCardsInHand ():
            self.deck.getStatus (self).drawCard ()
        if self.active_event is not None:
            npc = self.active_event.npc
            if npc is not None:
                try:
                    card = npc.drawCard (self, next_status = CARD_IN_PLAY)
                    self.resolve (location, card, played = False)
                except RuntimeError:
                    pass
        else:
            try:
                location.drawCard (self)
            except ValueError:
                pass
        
    def playCard (self, card):
        if not isinstance (card, CardStatus):
            cardstatus = card.getStatus (self)
        else:
            cardstatus = card
        return tuple (score + getattr (self, score.stat) for score in cardstatus.play ())
        
    def discard (self, number):
        # TODO Implement this
        print ("Discarding", number, "cards")
        self.deck.getStatus (self).discard (number)
        
    def sleep (self):
        """Reset all player temporaries, including reshuffling all decks and resetting all NPCs"""
        # Reshuffle all decks associated with the player
        for deckStatus in self.deckstatus_set.all ():
            deckStatus.reshuffle ()
        # Delete all npc instances; they'll be regenerated when the player interacts with them again
        for npcInstance in self.npcinstance_set.all ():
            npcInstance.delete ()
        
    def getCards (self, status = CARD_IN_PLAY, allDecks = False):
        query = CardStatus.objects.filter (deck__player = self).filter (status = status)
        if not allDecks:
            query = query.filter (deck__deck = self.deck)
        return query.all ()
        
    def addDeckStatus (self, deck):
        deckstatus = DeckStatus (deck = deck, player = self)
        deckstatus.save ()
        return deckstatus
        
    def attack (self, npc, scores):
        if scores == tuple ():
            return
        defenseStat, defenseValue = npc.defend (scores)
        if defenseValue < 0:
            print ("Immune")
            return
        if scores [0].stat == RESIST:
            print ("You can't attack with resist")
            return
        print (defenseStat)
        print (scores)
        damage = -defenseValue
        for stat, value in scores [:]:
            damage += value
            if OFFENSE_BONUS [stat] == defenseStat:
                # TODO Make this more visible to the player, possibly by passing it through score as a modifier
                # damage += 1
                pass
        if damage >= 0:
            print ("NPC took ", damage)
            npc.discard (damage)
        else:
            print ("You took ", damage)
            self.discard (-damage)
            
    def addEvent (self, cardStatus, event, location):
        """
        Add an active event to the event stack using the cardstatus as the appropriate card for that event
        
        cardStatus: a CardStatus object to associate with the new event
        event: an Event object to add to the event stack
        location: the Location object that identifies where the event takes place
        """
        event = ActiveEvent (player = self, cardStatus = cardStatus, event = event, stackOrder = self.activeevent_set.count (), location = location)
        event.log ()
        event.save ()
        
    def resolve (self, location, cardStatus = None, played = True):
        """
        Resolve anything unresolved on the stack.
        
        This first checks for any unresolved events on the stack. Then, if there are still events on the stack, it attempts to trigger a new event. At the end, it checks again for any unresolved events and resolves any free cards in play that aren't associated with events.
        
        location: The Location object where the resolution is taking place
        cardStatus: If a card was played this turn, it would get passed here. If no card was played, this is None
        
        returns: The topmost ActiveEvent object on the stack
        """
        # Check for unresolved events on the stack
        lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
        while lastEvent is not None and lastEvent.resolved:
            lastEvent.log ()
            lastEvent.delete ()
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
            
        # Attempt to trigger a new event using any cards that may have been played
        trigger = None
        failed = True
        if lastEvent is not None:
            trigger = lastEvent.resolve (self, cardStatus, played)
            if trigger is not None:
                log = TriggerLog (trigger = trigger, user = self, location = location, card = cardStatus.card)
                log.save ()
                if trigger.event is not None and not trigger.switch:
                    self.addEvent (cardStatus = cardStatus, event = trigger.event, location = location)
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
        elif cardStatus is not None:
            location.trigger_event (self, cardStatus)
            
        # Check for unresolved events on the stack
        while lastEvent is not None and lastEvent.resolved:
            lastEvent.log ()
            lastEvent.delete ()
            lastEvent = self.activeevent_set.order_by ("stackOrder").last ()
            
        # If the event is a switch event, resolve what you can, then add the next event
        if trigger is not None and trigger.switch and not failed:
            self.addEvent (cardStatus = cardStatus, event = trigger.event, location = location)
        
        # Resolve any free cards in play
        for card in self.getCards (CARD_IN_PLAY, True):
            try:
                if card.activeEvent is None:
                    card.resolve ()
            except ObjectDoesNotExist:
                card.resolve ()
                
        # Return the current event
        return lastEvent

# An actual player instance needs everything from the AbstractPlayer class but also a set of stats, which we define here dynamically in case we need to add more and to reduce redundancy between this and the CardTemplate classes
stats.update ({"__module__": __name__})
Player = type ('Player', (AbstractPlayer,), stats)

class Log (PolymorphicModel):
    event = models.ForeignKey ("events.Event", null =  True, blank = True)
    location = models.ForeignKey ("locations.Location")
    logged = models.DateTimeField (auto_now_add=True)
    card = models.ForeignKey (BaseCard, null = True, blank = True, default = None)
    
    user = models.ForeignKey (Player)
    
    # TODO these should use the flags associated with the log, not with the player directly
    
    @property
    def player (self):
        # TODO for convenience, clean this later
        return self.user
    
    @property
    def title (self):
        return Flag.parse (self.event.title, self.player, self)
    
    @property
    def content (self):
        return Flag.parse (self.event.content, self.player, self)

    class Meta:
        #Specify the order that the logging messages should appear "logged" for forward and "-logged" for reverse
        ordering = ['logged']
        
    def __repr__ (self):
        return "<Log Object %d>" % self.id
    
class TriggerLog (Log):
    trigger = models.ForeignKey ("events.EventTrigger")
    
    def __repr__ (self):
        return "<TriggerLog Object %d>" % self.id
    
    @property
    def title (self):
        return Flag.parse (self.trigger.title, self.player, self)
    
    @property
    def content (self):
        return Flag.parse (self.trigger.content, self.player, self)

class ActiveEvent (models.Model):
    player = models.ForeignKey (Player)
    event = models.ForeignKey ("events.Event")
    stackOrder = models.IntegerField ()
    cardStatus = models.OneToOneField (CardStatus, related_name = "activeEvent")
    resolved = models.BooleanField (default = False)
    logged = models.BooleanField (default = False)
    location = models.ForeignKey ("locations.Location", null = True)
    
    def getPrevious (self):
        if self.stackOrder <= 0:
            return None
        return self.player.active_events [self.stackOrder - 1]
    
    class Meta:
        unique_together = ("player", "event", "stackOrder")
        
    def __init__(self, *args, **kwargs):
        super(ActiveEvent, self).__init__(*args, **kwargs)
        
    def delete (self):
        if self.event.deck is not None:
            deckStatus = self.event.deck.getStatus (self.player, default = CARD_IN_HAND)
            deckStatus.delete ()
        super (ActiveEvent, self).delete ()
            
    def getCards (self, player, status):
        cards = []
        if self.event.deck is not None:
            deckStatus = self.event.deck.getStatus (self.player, default = CARD_IN_HAND)
            deckStatus.initialize (CARD_IN_HAND)
            cards = list (deckStatus.getCards (status).all ())

        previous = self.getPrevious ()
        if not self.event.blocking and previous is not None:
            return cards + previous.getCards (player, status)
        else:
            return cards
                
    def getLife (self):
        if self.event.life is not None:
            return self.event.life + self.event.generateNPCInstance (self.player).life
            
    life = property (getLife)
    
    def getNPC (self):
        if self.event is not None:
            return self.event.npc
            
    npc = property (getNPC)
    
    def resolve (self, player, cardStatus = None, played = True):
        trigger = self.event.resolve (player, cardStatus, played)
        if trigger is None and not self.event.blocking:
            previous = self.getPrevious ()
            if previous is not None:
                trigger = previous.resolve (player, cardStatus, played)
        if (trigger is not None and trigger.resolved) or self.event.auto:
            self.resolved = True
            self.save ()
        return trigger
            
    def log (self):
        if not self.logged:
            for eventeffect in self.event.eventeffect_set.all ():
                eventeffect.effect.affect (self.cardStatus.card.modifier, self.player, self.player.deck)
            
            log = Log (event = self.event, user = self.player, location = self.location)
            log.save ()
            flags = list (set ([LogFlag.fromPlayerFlag (flag.getPlayerFlag (self.player), log) for tag in self.event.contentFlags for flag in CompositeFlag.fromString (tag).getFlags ()]))
            [flag.save () for flag in flags]
            self.logged = True
            self.save ()
    
    @property
    def title (self):
        return Flag.parse (self.event.title, self.player)
    
    @property
    def content (self):
        return Flag.parse (self.event.content, self.player)
        
    def getHelper (self, template):
        trigger = self.event.eventtrigger_set.filter (template = template).order_by ("threshold").first ()
        if trigger is None:
            previous = self.getPrevious ()
            if previous is None:
                return ""
            else:
                return previous.getHelper (template)
        return trigger.helper
            
        
class Flag (models.Model):
    """A database entry that pertains to flags for the players"""
    
    name = models.CharField (max_length = 60, unique = True)
    
    def save (self, *args, **kwargs):
        if re.search ("(^[^a-zA-Z_]|[^a-zA-Z0-9_])", self.name) is not None:
            raise ValueError ("Flags must be valid python variables (a-zA-Z0-9 and can't begin with a number)")
        super (Flag, self).save (*args, **kwargs)
        
    @classmethod
    def get (cls, name):
        tag = cls.objects.filter (name = name).first ()
        if tag is None:
            raise ValueError ("No such flag", name)
        return tag
        
    def getFlags (self):
        return [self]
        
    def getPlayerFlag (self, player):
        flag = PlayerFlag.objects.filter (flag = self).filter (player = player).first ()
        if flag is None:
            flag = PlayerFlag (player = player, flag = self)
            flag.save ()
        return flag
            
    def getLogFlag (self, log):
        print ("Getting log flag", self.name)
        print (LogFlag.objects.all ())
        flag = LogFlag.objects.filter (flag = self).filter (log = log).first ()
        if flag is None:
            print ("Couldn't find flag", self.name)
            flag = LogFlag (log = log, flag = self)
            flag.save ()
        return flag
            
    def state (self, player, log = None):
        if log is None:
            return self.getPlayerFlag (player = player).state
        return self.getLogFlag (log = log).state
        
    def set (self, player, value):
        self.getPlayerFlag (player = player).state = value
        
    @classmethod
    def parse (cls, content, player, log = None):
        oldContent = None
        while "{" in content and content != oldContent:
            oldContent = content
            stack = []
            for i in range (len (content)):
                char = content [i]
                if char == "{":
                    stack.append (i)
                elif char == "}":
                    innerContent = content [stack [-1] + 1: i]
                    condition = innerContent.split ("?") [0]
                    success, failure = innerContent.split ("?") [1].split (":")
                    if CompositeFlag.fromString (condition).state (player = player, log = log):
                        content = content.replace (content [stack [-1]: i + 1], success)
                    else:
                        content = content.replace (content [stack [-1]: i + 1], failure)
                    break
        return content
        
    def __str__ (self):
        return self.name
        
    def __eq__ (self, other):
        return type (self) == type (other) and self.name == other.name
        
class CompositeFlag (object):
    def __init__ (self, *flags, operator = "and"):
        self.flags = flags
        self.operator = operator
        
    def getFlags (self):
        flags = []
        for flag in self.flags:
            if isinstance (flag, Flag):
                flags.append (flag)
            if isinstance (flag, CompositeFlag):
                flags += flag.getFlags ()
        return list (set (flags))
        
    def state (self, player, log = None):
        values = []
        for flag in self.flags:
            try:
                values.append (flag.state (player, log))
            except AttributeError:
                values.append (flag)

        if len (values) == 1:
            if self.operator == "not":
                return not values [0]
            return values [0]
                
        if self.operator == "and" or self.operator == "&&":
            return values [0] and CompositeFlag (*values [1:], operator = "and").state (player, log)
        if self.operator == "or" or self.operator == "||":
            return values [0] or CompositeFlag (*values [1:], operator = "or").state (player, log)
        if len (values) > 2:
            raise ValueError ("Unclear what it means to have three or more arguments to a binary operation")
        if self.operator == "is" or self.operator == "==":
            return values [0] == values [1]
        if self.operator == "!=":
            return values [0] != values [1]
        if self.operator == "+":
            return values [0] + values [1]
        if self.operator == "-":
            return values [0] - values [1]
        if self.operator == "*":
            return values [0] * values [1]
        if self.operator == "/":
            return values [0] / values [1]
        if self.operator == ">":
            return values [0] > values [1]
        if self.operator == "<":
            return values [0] < values [1]
        if self.operator == ">=":
            return values [0] >= values [1]
        if self.operator == "<=":
            return values [0] <= values [1]
        raise ValueError ("Unrecognized operator")
        
    @classmethod
    def fromString (cls, string):
        parse = ast.parse (string)
        if len (parse.body) > 1:
            raise RuntimeError ("Too complex")
        if len (parse.body) == 0:
            return cls (True)
        return cls.fromNode (parse.body [0].value)
                              
    @classmethod
    def fromNode (cls, node, opno = None):
        if isinstance (node, ast.Name):
            return Flag.get (node.id)
        if isinstance (node, ast.Num):
            return node.n
        if isinstance (node, ast.NameConstant):
            return node.value
        if isinstance (node, ast.BoolOp):
            op = node.op
            if isinstance (op, ast.And):
                return cls (*[cls.fromNode (value) for value in node.values], operator = "and")
            if isinstance (op, ast.Or):
                return cls (*[cls.fromNode (value) for value in node.values], operator = "or")
            raise ValueError ("Not implemented yet", type (node), type (op))
        if isinstance (node, ast.Compare):
            if opno is None and len (node.ops) > 1:
                return cls (*[cls.fromNode (node, opno = i) for i in range (len (node.ops))], operator = "and")
            if opno is None:
                opno = 0
            op = node.ops [opno]
            left = node.left if opno == 0 else node.comparators [opno - 1]
            right = node.comparators [opno]
            if isinstance (op, ast.Eq):
                return cls (cls.fromNode (left), cls.fromNode (right), operator = "==")
            if isinstance (op, ast.NotEq):
                return cls (cls.fromNode (left), cls.fromNode (right), operator = "!=")
            if isinstance (op, ast.Gt):
                return cls (cls.fromNode (left), cls.fromNode (right), operator = ">")
            if isinstance (op, ast.GtE):
                return cls (cls.fromNode (left), cls.fromNode (right), operator = ">=")
            if isinstance (op, ast.Lt):
                return cls (cls.fromNode (left), cls.fromNode (right), operator = "<")
            if isinstance (op, ast.LtE):
                return cls (cls.fromNode (left), cls.fromNode (right), operator = "<=")
            raise ValueError ("Not implemented yet", type (node), type (op))
        if isinstance (node, ast.BinOp):
            op = node.op
            if isinstance (op, ast.Add):
                return cls (cls.fromNode (node.left), cls.fromNode (node.right), operator = "+")
            if isinstance (op, ast.Sub):
                return cls (cls.fromNode (node.left), cls.fromNode (node.right), operator = "-")
            if isinstance (op, ast.Mult):
                return cls (cls.fromNode (node.left), cls.fromNode (node.right), operator = "*")
            if isinstance (op, ast.Div):
                return cls (cls.fromNode (node.left), cls.fromNode (node.right), operator = "/")
            raise ValueError ("Not implemented yet", type (node), type (op))
        if isinstance (node, ast.UnaryOp):
            op = node.op
            if isinstance (op, ast.Not):
                return cls (cls.fromNode (node.operand), operator = "not")
            raise ValueError ("Not implemented yet", type (node), type (op))
            

        raise ValueError ("Not implemented yet", type (node))
        
        
class PlayerFlag (models.Model):
    """A linking table that links flags to players"""
    
    player = models.ForeignKey (Player)
    flag = models.ForeignKey (Flag)
    state = models.IntegerField (default = 0)
    
    class Meta:
        unique_together = (('player', 'flag'))
        
    def __repr__ (self):
        return "<PlayerFlag %s for %s = %d>" % (str (self.flag), str (self.player), self.state)
        
    def __eq__ (self, other):
        return type (self) == type (other) and self.player == other.player and self.flag == other.flag and self.state == other.state
        
class LogFlag (models.Model):
    """A linking table that links flags to players"""
    
    log = models.ForeignKey (Log)
    flag = models.ForeignKey (Flag)
    state = models.IntegerField (default = 0)
    
    class Meta:
        unique_together = (('log', 'flag'))
        
    @classmethod
    def fromPlayerFlag (cls, playerFlag, log):
        return cls (log = log, flag = playerFlag.flag, state = playerFlag.state)
        
    def __repr__ (self):
        return "<LogFlag %s for %s = %d>" % (str (self.flag), str (self.log), self.state)
        
    def __eq__ (self, other):
        return type (self) == type (other) and self.log == other.log and self.flag == other.flag and self.state == other.state
        
    def __hash__ (self):
        return hash (self.log) + hash (self.flag)
    