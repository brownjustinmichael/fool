from django.db import models
import re
import ast

class Flag (models.Model):
    """A database entry that pertains to flags for the players"""
    
    name = models.CharField (max_length = 60, unique = True)
    temporary = models.BooleanField (default = False)
    
    @staticmethod
    def reset (player):
        for flag in player.playerflag_set.all ():
            if flag.flag.temporary:
                flag.delete ()
        night = Flag.get ("night")
        print (night.state (player))
        if night.state (player):
            night.set (player, 0)
        else:
            night.set (player, 1)
        night.save ()
        print (night.state (player))
            
    
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
        flag = LogFlag.objects.filter (flag = self).filter (log = log).first ()
        if flag is None:
            flag = LogFlag (log = log, flag = self)
            flag.save ()
        return flag
            
    def state (self, player, log = None):
        if log is None:
            return self.getPlayerFlag (player = player).state
        return self.getLogFlag (log = log).state
        
    def set (self, player, value):
        print (value)
        flag = self.getPlayerFlag (player = player)
        flag.state = value
        flag.save ()
        for flagDependency in self.flagdependency_set.all ():
            if flagDependency.independent_flag_value == value:
                flagDependency.dependent_flag.set (player, flagDependency.dependent_flag_value)
        
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
        
class FlagDependency (models.Model):
    """A database that links dependent flags together such that if one is changed, so too is the other."""
    
    independent_flag = models.ForeignKey (Flag)
    independent_flag_value = models.IntegerField (default = 0)
    dependent_flag = models.ForeignKey (Flag, related_name = "_unused_flagdependency_flag")
    dependent_flag_value = models.IntegerField (default = 0)
        
class CompositeFlag (object):
    def __init__ (self, *flags, **kwargs):
        self.flags = flags
        self.operator = kwargs.pop ("operator", "and")
        
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
    
    player = models.ForeignKey ("accounts.Player")
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
    
    log = models.ForeignKey ("accounts.Log")
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