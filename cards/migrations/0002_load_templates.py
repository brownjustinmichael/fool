# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from cards.models import PLAYER_STATS

def loadTemplates (apps, schema_editor):
    Template = apps.get_model ('cards', 'CardTemplate')
    db_alias = schema_editor.connection.alias
    
    Template.objects.using (db_alias).bulk_create ([
        Template (name = stat [1], stat = stat [0]) for stat in PLAYER_STATS
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RunPython (loadTemplates,)
    ]
