# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os
from sys import path
from django.core import serializers

def makePlayers (apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Player = apps.get_model("accounts", "Player")
    User = apps.get_model("auth", "User")
    db_alias = schema_editor.connection.alias
    
    Player.objects.using (db_alias).bulk_create ([
        Player (force = 3, user = user) for user in User.objects.all ()
    ])

class Migration(migrations.Migration):  

    dependencies = [
        ('accounts', '0002_card_log_player'),
    ]

    operations = [
        migrations.RunPython (makePlayers,),
    ]
