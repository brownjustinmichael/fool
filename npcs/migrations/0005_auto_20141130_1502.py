# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('npcs', '0004_npc_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='npcinstance',
            unique_together=set([('player', 'npc')]),
        ),
    ]
