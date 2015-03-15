# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20150314_2116'),
        ('npcs', '0004_remove_npc_life'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npclink',
            name='location',
        ),
        migrations.AddField(
            model_name='npclink',
            name='event',
            field=models.ForeignKey(to='events.Event', default=0),
            preserve_default=False,
        ),
    ]
