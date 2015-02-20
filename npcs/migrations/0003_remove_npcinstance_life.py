# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0002_npc_deck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npcinstance',
            name='life',
        ),
    ]
