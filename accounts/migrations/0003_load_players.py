# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os
from sys import path
from django.core import serializers

from cards.models import PLAYER_STATS
from accounts.models import CARD_IN_DECK

def makePlayers (apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Player = apps.get_model("accounts", "Player")
    User = apps.get_model("auth", "User")
    Card = apps.get_model("accounts", "Card")
    Template = apps.get_model("cards", "CardTemplate")
    db_alias = schema_editor.connection.alias
    
    Player.objects.using (db_alias).bulk_create ([
        Player (force = 3, user = user) for user in User.objects.all ()
    ])
    
    for player in Player.objects.all ():
        for stat in PLAYER_STATS:
            template = Template.objects.filter (stat = stat [0]).first ()
            Card.objects.using (db_alias).bulk_create ([
                Card (modifier = i + 1, player = player, status = CARD_IN_DECK, template = template) for i in range (getattr (player, stat [0]))
            ])
            

class Migration(migrations.Migration):  

    dependencies = [
        ('accounts', '0002_card_log_player'),
        ('cards', '0002_load_templates'),
    ]

    operations = [
        migrations.RunPython (makePlayers,),
    ]
